# Import os
import os

# Import tkinter
from tkinter import Tk

# Import pages
# from pages.EditorPage import EditorPage
# from pages.PlayerPage import PlayerPage
from pages.StartPage import StartPage
# from pages.ViewerPage import ViewerPage
# , PlayerPage, StartPage, ViewerPage

# This class will initalize the tkinter App


class App(Tk):  # Inherit Tk
    """Application Class"""

    def __init__(self):

        # Tk.__init__(self)
        # Initialize individual pages by module in the page folder
        StartPage()

        # TODO:
        # EditorPage.EditorPage()
        # PlayerPage.PlayerPage()
        # ViewerPage.ViewerPage()

        self.mainloop()


if __name__ == "__main__":
    App()
