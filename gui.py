import ttkbootstrap as ttkb
from os.path import join, expanduser
from utils import get_desktop
from tkinter import filedialog


class UserInterface:
    def __init__(self, root):
        self.root = root
        self.selected_dir = join(expanduser("~"), "Desktop")

        self.src_folder = ttkb.StringVar()
        self.dest_folder = ttkb.StringVar(value=str(get_desktop() / "Media_Backup"))
        self.is_photos_enabled = ttkb.BooleanVar(value=True)
        self.is_videos_enabled = ttkb.BooleanVar(value=True)
        self.is_audio_enabled = ttkb.BooleanVar(value=True)
        # self.pdf_var = ttkb.BooleanVar(value=False)
        # self.text_var = ttkb.BooleanVar(value=False)
        # self.zip_var = ttkb.BooleanVar(value=False)
        # self.document_var = ttkb.BooleanVar(value=False)
        self._running = False
        # self._stop_evt = threading.Event()

        self._build_ui()
        self._debug()

    def _build_ui(self):
        #! ── Source row ─────────────────────────────────────────────────────
        src_frame = ttkb.LabelFrame(self.root, text="Source folder")
        src_frame.pack(fill="x")

        ttkb.Entry(
            src_frame,
            textvariable=self.src_folder,
            width=60,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(6, 4),
            pady=6,
        )

        ttkb.Button(
            src_frame,
            text="Browse…",
            command=self._browse_src,
        ).pack(
            side="left",
            padx=(0, 6),
            pady=6,
        )

        #! ── Destination row ────────────────────────────────────────────────
        dest_frame = ttkb.LabelFrame(self.root, text="Destination folder")
        dest_frame.pack(fill="x")

        ttkb.Entry(
            dest_frame,
            textvariable=self.dest_folder,
            width=60,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(6, 4),
            pady=6,
        )

        ttkb.Button(
            dest_frame,
            text="Browse…",
            command=self._browse_dest,
        ).pack(
            side="left",
            padx=(0, 6),
            pady=6,
        )

        # ── Checkboxes ─────────────────────────────────────────────────────
        opt_frame = ttkb.LabelFrame(self.root, text="Extract")
        opt_frame.pack(fill="x")

        #! Row 1 — Media
        row1 = ttkb.Frame(opt_frame)
        row1.pack(fill="x", padx=4, pady=(6, 2))
        for var, label, emoji in (
            (self.is_photos_enabled, "Photos", "🖼️"),
            (self.is_videos_enabled, "Videos", "🎬"),
            (self.is_audio_enabled, "MP3 / Audio", "🎵"),
        ):
            ttkb.Checkbutton(row1, text=f"  {emoji}  {label}", variable=var).pack(
                side="left", padx=14
            )

        # Row 2 — Documents & Archives
        opt_text = ttkb.LabelFrame(opt_frame, text="Extra File Types")
        opt_text.pack(fill="x")

        # row2 = ttkb.Frame(opt_text)

        # row2.pack(fill="x", padx=4, pady=(2, 6))
        # for var, label, emoji in (
        #     (self.pdf_var, "PDFs", "📄"),
        #     (self.document_var, "Documents", "📝"),
        #     (self.text_var, "Text / Logs", "📃"),
        #     (self.zip_var, "Zip Files", "🗜️"),
        # ):
        #     ttkb.Checkbutton(row2, text=f"  {emoji}  {label}", variable=var).pack(
        #         side="left", padx=14
        #     )

        # # TODO ── Buttons ────────────────────────────────────────────────────────
        btn_frame = ttkb.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=(2, 0))

        self.start_btn = ttkb.Button(
            btn_frame,
            text="▶  Start",
            # command=self._start,
            style="Accent.TButton",
        )
        self.start_btn.pack(side="left", padx=(0, 6))

        self.stop_btn = ttkb.Button(
            btn_frame,
            text="⏹  Stop",
            # command=self._stop,
            state="disabled",
        )
        self.stop_btn.pack(side="left")

        # ttkb.Button(
        #     btn_frame,
        #     text="🗑  Clear log",
        #     # command=self._clear_log,
        # ).pack(
        #     side="right",
        # )

        # ── Progress bar ───────────────────────────────────────────────────
        self.progress = ttkb.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(6, 2))

        # ── Status counters ────────────────────────────────────────────────
        # stat_frame = ttkb.Frame(self.root)
        # stat_frame.pack(fill="x", padx=10)

        # self.lbl_copied = ttkb.Label(stat_frame, text="Copied: 0")
        # self.lbl_skipped = ttkb.Label(stat_frame, text="Skipped: 0")
        # self.lbl_errors = ttkb.Label(stat_frame, text="Errors: 0")
        # self.lbl_status = ttkb.Label(stat_frame, text="")

        # for w in (self.lbl_copied, self.lbl_skipped, self.lbl_errors):
        #     w.pack(side="left", padx=(0, 20))
        # self.lbl_status.pack(side="right")

        # ── Log area ───────────────────────────────────────────────────────
        log_frame = ttkb.LabelFrame(self.root, text="Log")
        log_frame.pack(fill="both", expand=True)

        self.log = ttkb.Text(
            log_frame,
            state="disabled",
            wrap="none",
            font=("Courier", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief="flat",
        )
        sb_y = ttkb.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        sb_x = ttkb.Scrollbar(log_frame, orient="horizontal", command=self.log.xview)
        self.log.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")
        self.log.pack(fill="both", expand=True)

        # Colour tags
        # self.log.tag_config(TAG_FOLDER, foreground="#569cd6")
        # self.log.tag_config(TAG_OK,     foreground="#4ec994")
        # self.log.tag_config(TAG_SKIP,   foreground="#888888")
        # self.log.tag_config(TAG_ERR,    foreground="#f44747")
        # self.log.tag_config(TAG_INFO,   foreground="#dcdcaa")
        # self.log.tag_config(TAG_DONE,   foreground="#c586c0")

    # ── Browse helpers ─────────────────────────────────────────────────────

    def _browse_src(self):
        if self.selected_dir != "/":
            self.selected_dir = filedialog.askdirectory(
                title="Select Source Folder", initialdir=self.selected_dir
            )
        else:
            self.selected_dir = filedialog.askdirectory(
                title="Select Source Folder", initialdir="/"
            )

        if self.selected_dir:
            self.src_folder.set(self.selected_dir)

    def _browse_dest(self):
        d = filedialog.askdirectory(title="Select destination folder")
        if d:
            self.dest_folder.set(d)

    def _debug(self):
        print(f"src_folder: {self.src_folder.get()}")
        print(f"dest_folder: {self.dest_folder.get()}")
        print(f"is_photos_enabled: {self.is_photos_enabled.get()}")
        print(f"is_videos_enabled: {self.is_videos_enabled.get()}")
        print(f"is_audio_enabled: {self.is_audio_enabled.get()}", end="\n\n")
        # print(f"pdf_var: {self.pdf_var.get()}")
        # print(f"text_var: {self.text_var.get()}")
        # print(f"zip_var: {self.zip_var.get()}")
        # print(f"document_var: {self.document_var.get()}", end="\n\n")
        self.root.after(2500, self._debug)
