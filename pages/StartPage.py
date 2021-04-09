#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tkinter import Button, Entry, Frame, Label, Menu, StringVar, messagebox
import tkinter.font as tkFont
import utils
from pages.ViewerPage import Viewer
from pages.PlayerPage import Player


class MainMenu():

    def __init__(self, master=None):

        self.root = master
        self.root.title("Main Menu")
        utils.set_window_center(self.root, 300, 180)
        self.username = StringVar()
        self.password = StringVar()
        self.init_page()

    def init_page(self):

        self.page = Frame(self.root)
        self.page.pack(pady=10)

        fontStyle = tkFont.Font(family="Lucida Grande", size=16)
        Label(self.page, text="Badminton Ladder Main Menu", font=fontStyle).grid(
            row=0, column=0)

        button_viewer = Button(self.page, text="Viewer", command=self.goViewer)
        button_viewer.grid(row=1, column=0, stick="NSEW", pady=8)
        button_player = Button(self.page, text="Player", command=self.goPlayer)
        button_player.grid(row=2, column=0, stick="NSEW", pady=8)
        button_editor = Button(self.page, text="Editor", command=self.goEditor)
        button_editor.grid(row=3, column=0, stick="NSEW", pady=8)

    def goViewer(self):
        self.page.destroy()
        Viewer(self.root)

    def goPlayer(self):
        self.page.destroy()
        Player(self.root)

    def goEditor(self):
        self.page.destroy()
        EditorPage(self.root)

    def doCancel(self):
        self.page.quit()

    def returnEnvent(self, event):
        self.doLogin()

    def isLoggedIn(self):
        # return True
        return False
