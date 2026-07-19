import os
import shutil
from pathlib import Path
from collections import defaultdict
from utils import (
    should_skip,
    TAG_INFO,
    TAG_ERR,
    TAG_FOLDER,
    TAG_OK,
    TAG_SKIP,
    TAG_DONE,
    IGNORED_KEYWORDS,
)


def run_backup(
    root: Path,
    dest_root: Path,
    active_exts: set,
    stop_event,
    log_cb,
    progress_cb,
    counters_cb,
    finish_cb,
):
    try:
        log_cb(f"🔍 Scanning: {root}", TAG_INFO)

        # --- 1. Scan Phase ---
        media_by_dir = defaultdict(list)
        for dirpath, dirnames, filenames in os.walk(root):
            if stop_event.is_set():
                break

            # Prune hidden & ignored folders on-the-fly
            dirnames[:] = [
                d
                for d in dirnames
                if not d.startswith(".")
                and not any(kw in d.lower() for kw in IGNORED_KEYWORDS)
            ]

            current_dir = Path(dirpath)
            if should_skip(current_dir.parts):
                continue

            for filename in filenames:
                if (
                    not filename.startswith(".")
                    and Path(filename).suffix.lower() in active_exts
                ):
                    media_by_dir[current_dir].append(current_dir / filename)

        media_by_dir = {d: f for d, f in media_by_dir.items() if f}

        if not media_by_dir:
            log_cb("⚠️ No matching media files found.", TAG_ERR)
            finish_cb()
            return

        total_folders = len(media_by_dir)
        total_files = sum(len(f) for f in media_by_dir.values())

        log_cb(
            f"📋 Found {total_files:,} file(s) in {total_folders:,} folder(s) → Dest: {dest_root}",
            TAG_INFO,
        )
        progress_cb(0, total_files)

        copied = already = errored = 0

        # --- 2. Copy Phase ---
        for folder_idx, (source_dir, files) in enumerate(media_by_dir.items(), 1):
            if stop_event.is_set():
                log_cb("⏹ Stopped by user.", TAG_ERR)
                break

            rel = (
                source_dir.relative_to(root)
                if root in source_dir.parents
                else Path(source_dir.name)
            )
            dest_dir = dest_root / rel
            dest_dir.mkdir(parents=True, exist_ok=True)

            log_cb(
                f"📂 [{folder_idx}/{total_folders}] {rel if str(rel) != '.' else '(root)'} — {len(files)} file(s)",
                TAG_FOLDER,
            )

            for src_file in files:
                if stop_event.is_set():
                    break

                dest_file = dest_dir / src_file.name
                total_processed = copied + already + errored

                if dest_file.exists():
                    already += 1
                    log_cb(
                        f"   Skip -> [{total_processed+1}/{total_files}] {src_file.name} (exists)",
                        TAG_SKIP,
                    )
                else:
                    try:
                        shutil.copy2(src_file, dest_file)
                        copied += 1
                        log_cb(
                            f"   OK   -> [{total_processed+1}/{total_files}] {src_file.name}",
                            TAG_OK,
                        )
                    except Exception as exc:
                        errored += 1
                        log_cb(
                            f"   ERR  -> [{total_processed+1}/{total_files}] {src_file.name} -> {exc}",
                            TAG_ERR,
                        )

                progress_cb(copied + already + errored, total_files)
                counters_cb(copied, already, errored, "Running...")

        # --- 3. Summary Phase ---
        log_cb("\n" + "=" * 56, TAG_DONE)
        log_cb("  📊 COMPLETE", TAG_DONE)
        log_cb("=" * 56, TAG_DONE)
        log_cb(f"  ✅ Copied   : {copied:,}", TAG_OK)
        log_cb(f"  ⏭ Skipped  : {already:,}", TAG_SKIP)
        if errored:
            log_cb(f"  ⚠️ Errors   : {errored:,}", TAG_ERR)
        log_cb("=" * 56, TAG_DONE)

        counters_cb(copied, already, errored, "Done ✓")
        progress_cb(total_files, total_files)

    except Exception as exc:
        log_cb(f"❌ Unexpected error: {exc}", TAG_ERR)
    finally:
        finish_cb()
