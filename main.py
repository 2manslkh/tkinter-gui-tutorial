# Import os
import os

# Import tkinter
from tkinter import Tk

# Import pages
from pages import StartPage


# This class will initalize the tkinter App
class App(Tk):
    """Application Class"""

    def __init__(self):

        Tk.__init__(self)

        # Login Window
        StartPage.MainMenu(self)

        self.mainloop()


if __name__ == "__main__":
    App()
