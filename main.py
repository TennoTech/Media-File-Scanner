import ttkbootstrap as ttkb
from gui import UserInterface


class MainApplication:
    def __init__(self):
        self.root = ttkb.Window(
            title="Media Scanner",
            size=[750, 520],
        )
        self.root.place_window_center(100)

        UserInterface(self.root)

        self.root.mainloop()


MainApplication()
