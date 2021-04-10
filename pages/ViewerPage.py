#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    Menu,
    StringVar,
    messagebox,
    Canvas,
    LabelFrame,
    ttk,
    Grid,
    Tk,
)
import utils

from tkcalendar import Calendar, DateEntry

import pages

from components import ladder

from datetime import datetime

from collections import defaultdict


class Viewer:
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

        self.var_position = StringVar()
        self.var_name = StringVar()
        self.var_win_loss = StringVar()
        self.var_next_challenger = StringVar()
        self.results_1 = StringVar()
        self.results_1.set("Results 1")
        self.results_2 = StringVar()
        self.results_2.set("Results 2")
        self.results_3 = StringVar()
        self.results_3.set("Results 3")
        self.results_4 = StringVar()
        self.results_4.set("Results 4")

        self.name_filter = StringVar()
        self.name_filter.set("Input Name")

        self.hist_leaderboard_date = StringVar()
        self.hist_leaderboard_date.set("Input Date: DD-MM-YY")
        self.init_ladder()
        self.init_page()

    def init_ladder(self):

        self.left_frame = Frame(self.root)
        self.left_frame.pack(side="left", anchor="w")

        # Back Button
        Button(self.left_frame, text="<<< Back", command=self.goBack, bg="red").pack(
            side="top", fill="both"
        )

        # Tree View
        self.ladder = ttk.Treeview(
            self.left_frame, show="headings", height=600)
        self.ladder.pack(side="left")

        # Column Names
        self.ladder["columns"] = ("#", "Name")

        self.ladder.column("#", width=25)
        self.ladder.column("Name", width=175)

        self.ladder.heading("#", text="#")
        self.ladder.heading("Name", text="Name")

        self.resetTreeView(self.ladder)
        # Load Ladder Data
        self.loadLadderData()

        self.ladder.bind("<<TreeviewSelect>>", self.displayData)

    def goBack(self):

        self.footer_frame.destroy()
        self.body_frame.destroy()
        self.head_frame.destroy()
        # self.right_frame.destroy()
        self.ladder.destroy()
        self.left_frame.destroy()
        pages.StartPage.MainMenu(self.root)
        # self.root.destroy()

    # Load ladder data into tree view
    def loadLadderData(self):

        for pos, name in enumerate(self.ladder_data):
            self.ladder.insert(
                "",
                "end",
                text="",
                values=(pos + 1, name),
            )

    # Load historical ladder data into tree view
    def loadHistoricalLadderData(self, historical_ladder):
        self.resetTreeView(self.ladder)
        for pos, name in enumerate(historical_ladder):
            self.ladder.insert(
                "",
                "end",
                text="",
                values=(pos + 1, name),
            )

    def init_page(self):

        self.right_frame = Frame(self.root).pack(side="right", anchor="e")

        # ----- Header Frame -----
        self.head_frame = LabelFrame(
            self.right_frame, text="Player Information", height=300
        )
        self.head_frame.pack(fill="both", expand=0)

        # Player Data
        # Position
        Label(self.head_frame, textvariable=self.var_position).pack(anchor="w")
        # Name
        Label(self.head_frame, textvariable=self.var_name).pack(anchor="w")
        # Win/Loss
        Label(self.head_frame, textvariable=self.var_win_loss).pack(anchor="w")
        # Next Challenge
        Label(self.head_frame, textvariable=self.var_next_challenger).pack(anchor="w")

        # ----- Body Frame -----
        # User options
        self.body_frame = LabelFrame(self.right_frame, text="Options")
        self.body_frame.pack(fill="both", expand="yes")

        # Most Active Player Button
        button_most_active_player = Button(
            self.body_frame, text="Most Active Player", command=self.getMostActivePlayer
        )
        button_most_active_player.grid(row=0, column=0, sticky="EW")

        # Least Active Player Button
        button_least_active_player = Button(
            self.body_frame,
            text="Least Active Player",
            command=self.getLeastActivePlayer,
        )
        button_least_active_player.grid(row=0, column=1, sticky="W")

        # Display for Most/Least Active Player
        results_1_display = Label(self.body_frame, textvariable=self.results_1)
        results_1_display.grid(
            row=1, column=0, columnspan=7, stick="W", pady=10)

        # Historical Leaderboard Button
        button_historical_leaderboard = Button(
            self.body_frame,
            text="View Historical Leaderboard",
            command=self.getHistoricalLeaderboard,
        )
        button_historical_leaderboard.grid(row=2, column=0, sticky="EW")

        # Historical Leaderboard Input
        self.date_entry = DateEntry(
            self.body_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/y",
        )
        self.date_entry.grid(row=2, column=1, padx=(10, 100))

        # ----- Footer Frame -----
        # Upcoming Challenges
        self.footer_frame = Frame(self.right_frame)
        self.footer_frame.pack(fill="both")

        button_all_matches = Button(
            self.footer_frame, text="All", command=self.getAllMatches
        )
        button_all_matches.grid(row=0, column=0, sticky="W")

        button_upcoming_matches = Button(
            self.footer_frame, text="Upcoming", command=self.getUpcomingMatches
        )
        button_upcoming_matches.grid(row=0, column=1, sticky="W")

        button_filter_by_name = Button(
            self.footer_frame, text="Filter by Name", command=self.getMatchesByName
        )
        button_filter_by_name.grid(row=0, column=2, sticky="W")

        self.entry_name_filter = Entry(
            self.footer_frame, textvariable=self.name_filter)
        self.entry_name_filter.grid(row=0, column=3, sticky="W")

        button_filter_by_date = Button(
            self.footer_frame, text="Filter by Date", command=self.getMatchesByDate
        )
        button_filter_by_date.grid(row=0, column=4, sticky="W")

        # Historical Leaderboard Input
        self.date_entry_start = DateEntry(
            self.footer_frame,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/y",
        )
        self.date_entry_start.grid(row=0, column=5, sticky="W")

        # Historical Leaderboard Input
        self.date_entry_end = DateEntry(
            self.footer_frame,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/y",
        )
        self.date_entry_end.grid(row=0, column=6, sticky="W")

        # Tree View
        self.upcoming_challenges = ttk.Treeview(
            self.footer_frame, show="headings")
        self.upcoming_challenges.grid(column=0, row=1, columnspan=7)

        # Column Names
        self.upcoming_challenges["columns"] = (
            "Match Date",
            "Player 1",
            "Player 2",
            "Match 1",
            "Match 2",
            "Match 3",
            "Winner",
        )

        self.upcoming_challenges.column("Match Date", width=100)
        self.upcoming_challenges.column("Player 1", width=90)
        self.upcoming_challenges.column("Player 2", width=90)
        self.upcoming_challenges.column("Match 1", width=70)
        self.upcoming_challenges.column("Match 2", width=70)
        self.upcoming_challenges.column("Match 3", width=70)
        self.upcoming_challenges.column("Winner", width=98)

        self.upcoming_challenges.heading("Match Date", text="Match Date")
        self.upcoming_challenges.heading("Player 1", text="Player 1")
        self.upcoming_challenges.heading("Player 2", text="Player 2")
        self.upcoming_challenges.heading("Match 1", text="Match 1")
        self.upcoming_challenges.heading("Match 2", text="Match 2")
        self.upcoming_challenges.heading("Match 3", text="Match 3")
        self.upcoming_challenges.heading("Winner", text="Winner")

    def getAllMatches(self):
        self.resetTreeView(self.upcoming_challenges)
        for data in self.match_data:
            if data["action"] == "result":
                # Default Dictionary that returns '-' if key error
                results = defaultdict(lambda: "-")
                results[0] = "-"
                results[1] = "-"
                results[2] = "-"
                winner = utils.determine_winner(data["results"])

                if winner == 0:
                    winner = data["name_1"]
                elif winner == 1:
                    winner = data["name_2"]
                else:
                    winner = "TBA"

                for i in range(len(data["results"])):
                    if results[i] != "":
                        results[i] = data["results"][i]

                self.upcoming_challenges.insert(
                    "",
                    "end",
                    text="",
                    values=(
                        data["date"].strftime("%d-%m-%y"),
                        data["name_1"],
                        data["name_2"],
                        results[0],
                        results[1],
                        results[2],
                        winner,
                    ),
                )

        print("get all matches")

    def getUpcomingMatches(self):

        self.resetTreeView(self.upcoming_challenges)
        for data in self.match_data:
            if data["date"] >= datetime.now():
                if data["action"] == "result":
                    # Default Dictionary that returns '-' if key error
                    results = defaultdict(lambda: "-")
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"
                    winner = utils.determine_winner(data["results"])
                    if winner == 0:
                        winner = data["name_1"]
                    elif winner == 1:
                        winner = data["name_2"]
                    else:
                        winner = "TBA"

                    for i in range(len(data["results"])):
                        if results[i] != "":
                            results[i] = data["results"][i]

                    self.upcoming_challenges.insert(
                        "",
                        "end",
                        text="",
                        values=(
                            data["date"].strftime("%d-%m-%y"),
                            data["name_1"],
                            data["name_2"],
                            results[0],
                            results[1],
                            results[2],
                            winner,
                        ),
                    )

    def resetTreeView(self, tree):
        tree.delete(*tree.get_children())

    def getMatchesByDate(self):
        print("get matches by date")
        self.resetTreeView(self.upcoming_challenges)
        for data in self.match_data:
            if (
                data["date"].date() >= self.date_entry_start.get_date()
                and data["date"].date() <= self.date_entry_end.get_date()
            ):
                if data["action"] == "result":
                    # Default Dictionary that returns '-' if key error
                    results = defaultdict(lambda: "-")
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"
                    winner = utils.determine_winner(data["results"])
                    if winner == 0:
                        winner = data["name_1"]
                    elif winner == 1:
                        winner = data["name_2"]
                    else:
                        winner = "TBA"

                    for i in range(len(data["results"])):
                        if results[i] != "":
                            results[i] = data["results"][i]

                    self.upcoming_challenges.insert(
                        "",
                        "end",
                        text="",
                        values=(
                            data["date"].strftime("%d-%m-%y"),
                            data["name_1"],
                            data["name_2"],
                            results[0],
                            results[1],
                            results[2],
                            winner,
                        ),
                    )

    def getMatchesByName(self):
        print("get matches by name")
        self.resetTreeView(self.upcoming_challenges)
        for data in self.match_data:
            if (
                data["name_1"] == self.name_filter.get()
                or data["name_2"] == self.name_filter.get()
            ):
                if data["action"] == "result":
                    # Default Dictionary that returns '-' if key error
                    results = defaultdict(lambda: "-")
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"

                    winner = utils.determine_winner(data["results"])
                    if winner == 0:
                        winner = data["name_1"]
                    elif winner == 1:
                        winner = data["name_2"]
                    else:
                        winner = "TBA"

                    for i in range(len(data["results"])):
                        if results[i] != "":
                            results[i] = data["results"][i]

                    self.upcoming_challenges.insert(
                        "",
                        "end",
                        text="",
                        values=(
                            data["date"].strftime("%d-%m-%y"),
                            data["name_1"],
                            data["name_2"],
                            results[0],
                            results[1],
                            results[2],
                            winner,
                        ),
                    )

    def getHistoricalLeaderboard(self):
        selected_date = self.date_entry.get_date()
        historical_ladder = utils.LadderFile.get_historical_ladder(
            selected_date)
        self.loadHistoricalLadderData(historical_ladder)

    def displayData(self, event):

        selection = event.widget.selection()[0]
        self.selected_item = self.ladder.item(selection)
        values = self.selected_item["values"]
        self.var_position.set(f"Current Position: {values[0]}")
        self.var_name.set(f"Name: {values[1]}")

    def getMostActivePlayer(self):
        max_matches_played = max(self.matches_played.values())
        most_active_player = [
            name
            for (name, total_matches) in self.matches_played.items()
            if total_matches == max_matches_played
        ]
        self.results_1.set(
            f"Most Active Players: {str(', '.join(most_active_player))} ({max_matches_played} matche(s))")

    def getLeastActivePlayer(self):
        min_matches_played = min(self.matches_played.values())
        least_active_player = [
            name
            for (name, total_matches) in self.matches_played.items()
            if total_matches == min_matches_played
        ]
        self.results_1.set(
            f"Least Active Players: {str(', '.join(least_active_player))} ({min_matches_played} matche(s))")
