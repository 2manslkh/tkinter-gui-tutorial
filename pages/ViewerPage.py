#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tkinter import Button, Entry, Frame, Label, Menu, StringVar, messagebox, Canvas, LabelFrame
import utils
# import lib.dbcontent as dbcontent
# import lib.global_variable as glv
from pages import ViewerPage, PlayerPage, EditorPage
from components import ladder
# from lib.functions import set_window_center


class Viewer():
    """登录"""

    def __init__(self, master=None):

        self.root = master
        self.root.title("Badminton Ladder")
        self.w = 800
        self.h = 600
        utils.set_window_center(self.root, self.w, self.h)
        self.var_position = StringVar()
        self.var_name = StringVar()
        self.var_win_loss = StringVar()
        self.var_next_challenger = StringVar()
        self.init_page()

    def init_page(self):

        # Load Data
        self.displayData("1", "Best Player", "100", "0", "Loser", "10/05/2021")

        left_frame = Frame(self.root).pack(side='left', anchor="w")
        # left_canvas = Canvas(left_frame, bg="white",
        #                      width=100, height=self.h).pack(side='left')
        # left_frame.pack(side='left', expand=0, anchor="nw")

        self.player_ladder = ladder.Ladder(left_frame)
        self.player_ladder.pack(side='left')

        # Load Ladder Data
        self.player_ladder.loadLadderData(utils.LadderFile.get_ladder())

        right_frame = Frame(self.root).pack(side='right', anchor="e")
        # right_frame.pack(side='left', expand=1)
        # # canvas = Canvas(right_frame, width=600, height=600, bg="white")
        # # back_button = Button(right_frame, text="Back", command=self.goBack)

        head_frame = LabelFrame(
            right_frame, text="Player Information", height=300)
        head_frame.pack(fill="both", expand=0)
        # Player Data
        # Position
        Label(head_frame, textvariable=self.var_position,
              justify='left').pack(anchor="w")
        # Name
        Label(head_frame, textvariable=self.var_name).pack(anchor="w")
        # Win/Loss
        Label(head_frame, textvariable=self.var_win_loss).pack(anchor="w")
        # Next Challenge
        Label(head_frame, textvariable=self.var_next_challenger).pack(anchor="w")

        # head_canvas = Canvas(head_frame, bg="blue").pack(
        #     side='top', fill="both")

        body_frame = LabelFrame(right_frame, text="Options").pack(
            fill="both", expand="yes")

        # head_canvas = Canvas(head_frame, bg="white").pack()
        # # head_frame.grid(row=0, column=0)
        # Label(head_frame, text='test').pack(side='left')

        # head_frame = LabelFrame(self, text="文章操作")
        # head_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")
        # Label(head_frame, textvariable=self.selected_name).pack()

        # Label(right_frame, text='').pack()
        # canvas.create_text(150, 50, text="Badminton Ladder",
        #                    font="time 20", tags="string", justify="left")
        # canvas.pack(anchor="nw")

    def displayData(self, position, name, wins, losses, challenger_name, challenge_date):
        self.var_position.set(f"Current Position: {position}")
        self.var_name.set(f"Name: {name}")
        self.var_win_loss.set(f"Wins: {wins} | Losses: {losses}")
        self.var_next_challenger.set(
            f"Next Challenger: {challenger_name} ({challenge_date})")

    def goViewer(self):
        self.page.destroy()
        ViewerPage(self.root)

    def goPlayer(self):
        self.page.destroy()
        PlayerPage(self.root)

    def goEditor(self):
        self.page.destroy()
        EditorPage(self.root)

    def goBack(self):
        self.page.destroy()
        StartPage(self.root)

    def doCancel(self):
        self.page.quit()

    def returnEnvent(self, event):
        self.doLogin()

    def isLoggedIn(self):
        # return True
        return False
