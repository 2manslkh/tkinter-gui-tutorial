# Import os
import os

# Import tkinter
from tkinter import Tk

# Import pages
# from pages.EditorPage import EditorPage
# from pages.PlayerPage import PlayerPage
from pages import StartPage
# from pages.ViewerPage import ViewerPage
# , PlayerPage, StartPage, ViewerPage
# from components.base import Base

# This class will initalize the tkinter App


class App(Tk):
    """Application Class"""

    def __init__(self):

        Tk.__init__(self)

        # Login Window
        StartPage.MainMenu(self)
        # StartPage.Start(self)

        self.mainloop()


if __name__ == "__main__":
    App()
