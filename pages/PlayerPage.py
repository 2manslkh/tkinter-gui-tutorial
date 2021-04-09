#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tkinter import Button, Entry, Frame, Label, Menu, StringVar, messagebox, Canvas, LabelFrame, ttk, Grid, Tk
import utils

from tkcalendar import Calendar, DateEntry

import pages

from components import ladder

from datetime import datetime

from collections import defaultdict


class Player():

    def __init__(self, master=None):

        self.root = master
        self.root.title("Badminton Ladder")
        self.w = 800
        self.h = 600
        utils.set_window_center(self.root, self.w, self.h)

        # Load Data from txt files
        self.ladder_data = utils.LadderFile.get_ladder()
        self.match_data = utils.DataFile.get_data()
        self.matches_played = utils.calculate_matches_played(self.match_data)

        self.player_name = StringVar()

        # Init Page
        self.init_page()

    def init_page(self):

        self.page = Frame(self.root)
        self.page.pack(fill='both')

        top_frame = Frame(self.page)
        top_frame.pack(fill='both', side='top')

        # Back Button
        Button(top_frame, text="<<< Back",
               command=self.goBack, bg='red').grid(row=0, column=0, sticky="W")

        self.entry_name = Entry(
            top_frame, textvariable=self.player_name)

        self.entry_name.grid(row=1, column=0, columnspan=3,
                             padx=(310, 400), sticky="WE")

        button_set_player = Button(
            top_frame, text="Set Player", command=self.setPlayer)
        button_set_player.grid(row=2, column=0, sticky="WE", padx=(310, 0))

        button_register = Button(
            top_frame, text="Register", command=self.register)
        button_register.grid(row=2, column=1, sticky="WE")

        button_withdraw = Button(
            top_frame, text="Withdraw", command=self.withdraw)
        button_withdraw.grid(row=2, column=2, sticky="WE", padx=(0, 400))

        self.create_match_frame = LabelFrame(self.page, text="Create Match")
        self.create_match_frame.pack(fill='both', side='bottom')

        Canvas(self.create_match_frame, bg='white').pack()

    def goBack(self):
        pass
        # self.footer_frame.destroy()
        # self.body_frame.destroy()
        # self.head_frame.destroy()
        # # self.right_frame.destroy()
        # self.left_frame.destroy()
        # pages.StartPage.MainMenu(self.root)
        # # self.root.destroy()

    def setPlayer(self):
        pass

    def withdraw(self):
        pass

    def register(self):
        pass
