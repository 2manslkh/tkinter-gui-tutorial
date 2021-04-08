#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from tkinter import Canvas, Label, Tk

import utils


class StartPage(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Start Page")
        self.w = 300
        self.h = 600
        utils.set_window_center(self, self.w, self.h)
        self.resizable(False, False)
        self.create()

    def create(self):

        canvas = Canvas(self, width=self.w, height=self.h, bg="white")

        canvas.create_text(
            self.w / 2, self.h / 6, text="Badminton Ladder", font="time 20", tags="string"
        )

        # Create Viewer Button

        # Create Player Button

        # Create Editor Button

        Label(self, text="Jefri Tan", bg="green", fg="#fff", height=2).pack(
            fill="both", side="bottom"
        )
        canvas.pack(fill="both")

        self.mainloop()
