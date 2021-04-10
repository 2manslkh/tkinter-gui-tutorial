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


class Player:
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
        print(self.matches_played)

        self.player_name = StringVar()
        self.opponent_name = StringVar()
        self.alert_msg_1 = StringVar()
        self.alert_msg_2 = StringVar()
        self.alert_msg_3 = StringVar()

        self.game_1_score = StringVar()
        self.game_2_score = StringVar()
        self.game_3_score = StringVar()

        # Init Page
        self.init_page()
        self.getUpcomingMatches()

    def init_page(self):

        self.page = Frame(self.root)
        self.page.pack(fill="both")

        top_frame = Frame(self.page)
        top_frame.pack(fill="both", side="top")

        # Back Button
        Button(top_frame, text="<<< Back", command=self.goBack, bg="red").grid(
            row=0, column=0, sticky="W"
        )

        # Input Name text
        Label(top_frame, text="Input Player Name: ").grid(
            row=1, column=0, padx=(10, 0), pady=(10, 10), sticky="WE"
        )

        # Player Name Input Box
        self.entry_name = Entry(top_frame, textvariable=self.player_name)

        self.entry_name.grid(row=1, column=1, padx=(
            0, 10), pady=(10, 10), sticky="WE")

        button_register = Button(
            top_frame, text="Register", command=self.register)
        button_register.grid(row=1, column=2, sticky="WE")

        button_withdraw = Button(
            top_frame, text="Withdraw", command=self.withdraw)
        button_withdraw.grid(row=1, column=3, sticky="WE", padx=(0, 0))

        # Input Name Alert
        Label(top_frame, textvariable=self.alert_msg_1).grid(
            row=1, column=4, padx=(10, 0), pady=(10, 10), sticky="WE"
        )

        # ----- Create Match -----
        self.create_match_frame = LabelFrame(self.page, text="Create Match")
        self.create_match_frame.pack(fill="both", side="top")

        # Opponent Name Text
        Label(self.create_match_frame, text="Opponent Name: ").grid(
            row=0, column=0, sticky="WE", pady=(10, 10), padx=(10, 5)
        )

        # Opponent Name Entry
        self.entry_opponent_name = Entry(
            self.create_match_frame, textvariable=self.opponent_name
        )
        self.entry_opponent_name.grid(
            row=0, column=1, sticky="WE", pady=(10, 10))

        # Match Date Text
        Label(self.create_match_frame, text="Match Date: ").grid(
            row=0, column=2, sticky="WE", pady=(10, 10), padx=(10, 0)
        )

        # Match Date Input
        self.dateentry_create_match = DateEntry(
            self.create_match_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/y",
        )
        self.dateentry_create_match.grid(row=0, column=3, pady=(10, 10))

        button_create_match = Button(
            self.create_match_frame, text="Create Match", command=self.createMatch
        )
        button_create_match.grid(
            row=0, column=4, sticky="WE", padx=(20, 0), pady=(10, 10)
        )

        # Create Match Alert
        Label(self.create_match_frame, textvariable=self.alert_msg_2).grid(
            row=0, column=5, padx=(10, 0), pady=(10, 10), sticky="WE"
        )

        # ----- Upcoming Challenges -----
        self.challenges_frame = Frame(self.page)
        self.challenges_frame.pack(fill="both", side="top")
        # Tree View
        self.upcoming_challenges = ttk.Treeview(
            self.challenges_frame, show="headings")
        self.upcoming_challenges.grid(column=0, row=1, columnspan=7)

        # Column Names
        self.upcoming_challenges["columns"] = (
            "id",
            "Match Date",
            "Player 1",
            "Player 2",
            "Match 1",
            "Match 2",
            "Match 3",
            "Winner",
        )

        self.upcoming_challenges.column("id", width=10)
        self.upcoming_challenges.column("Match Date", width=100)
        self.upcoming_challenges.column("Player 1", width=110)
        self.upcoming_challenges.column("Player 2", width=110)
        self.upcoming_challenges.column("Match 1", width=110)
        self.upcoming_challenges.column("Match 2", width=110)
        self.upcoming_challenges.column("Match 3", width=110)
        self.upcoming_challenges.column("Winner", width=140)

        self.upcoming_challenges.heading("id", text="id")
        self.upcoming_challenges.heading("Match Date", text="Match Date")
        self.upcoming_challenges.heading("Player 1", text="Player 1")
        self.upcoming_challenges.heading("Player 2", text="Player 2")
        self.upcoming_challenges.heading("Match 1", text="Match 1")
        self.upcoming_challenges.heading("Match 2", text="Match 2")
        self.upcoming_challenges.heading("Match 3", text="Match 3")
        self.upcoming_challenges.heading("Winner", text="Winner")

        self.upcoming_challenges.bind("<<TreeviewSelect>>", self.displayData)

        # ----- Edit Score -----
        self.edit_score_frame = LabelFrame(self.page, text="Edit Score")
        self.edit_score_frame.pack(fill="both", side="bottom")

        Label(self.edit_score_frame, text="Game 1").grid(
            row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="W"
        )
        Label(self.edit_score_frame, text="Game 2").grid(
            row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="W"
        )
        Label(self.edit_score_frame, text="Game 3").grid(
            row=0, column=2, padx=(10, 10), pady=(10, 0), sticky="W"
        )

        self.entry_game_1 = Entry(
            self.edit_score_frame, textvariable=self.game_1_score)

        self.entry_game_1.grid(
            row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="WE"
        )

        self.entry_game_2 = Entry(
            self.edit_score_frame, textvariable=self.game_2_score)

        self.entry_game_2.grid(row=1, column=1, padx=(
            0, 10), pady=(0, 10), sticky="WE")

        self.entry_game_3 = Entry(
            self.edit_score_frame, textvariable=self.game_3_score)

        self.entry_game_3.grid(row=1, column=2, padx=(
            0, 10), pady=(0, 10), sticky="WE")

        button_edit = Button(
            self.edit_score_frame, text="Update Score", command=self.updateScore
        )
        button_edit.grid(row=1, column=3, padx=(
            0, 10), pady=(0, 10), sticky="WE")

        # Input Name Alert
        Label(self.edit_score_frame, textvariable=self.alert_msg_3).grid(
            row=1, column=4, padx=(10, 0), pady=(0, 10), sticky="WE"
        )

    def updateScore(self):
        print("update score")
        idx = self.selected_item_id

        game_1_score = self.game_1_score.get()
        game_2_score = self.game_2_score.get()
        game_3_score = self.game_3_score.get()

        if (
            self.checkIfCorrectScoreFormat(game_1_score)
            and self.checkIfCorrectScoreFormat(game_2_score)
            and self.checkIfCorrectScoreFormat(game_3_score)
        ):

            results = [game_1_score, game_2_score, game_3_score]
            self.match_data[idx]["results"] = results
            utils.DataFile.write_data_file_from_data_list(self.match_data)
            self.getUpcomingMatches()
            self.alert_msg_3.set("Score Updated!")

        else:
            self.alert_msg_3.set("Invalid Format, use <int>-<int>")

        self.updateLadder()

    def updateLadder(self):
        winner = utils.determine_winner(
            self.match_data[self.selected_item_id]["results"]
        )
        if winner == 0:
            winner = self.match_data[self.selected_item_id]["name_1"]
        elif winner == 1:
            winner = self.match_data[self.selected_item_id]["name_2"]
        print(self.selection_player_1)
        print(winner)
        if winner == self.selection_player_1:
            print(
                f"{self.selection_player_1} won and will swap position with {self.selection_player_2}"
            )
            utils.LadderFile.update_position(
                self.selection_player_1, self.selection_player_2
            )

    def displayData(self, event):

        selection = event.widget.selection()[0]
        self.selected_item = self.upcoming_challenges.item(selection)
        values = self.selected_item["values"]
        self.selected_item_id = values[0]

        self.game_1_score.set(f"{values[4]}")
        self.game_2_score.set(f"{values[5]}")
        self.game_3_score.set(f"{values[6]}")
        self.selection_player_1 = values[2]
        self.selection_player_2 = values[3]

    def getUpcomingMatches(self):

        self.match_data = utils.DataFile.get_data()
        self.resetTreeView(self.upcoming_challenges)

        for idx, data in enumerate(self.match_data):
            if data["date"] >= datetime.now() or data["results"] == []:
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
                            idx,
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

    def createMatch(self):
        player_1 = self.player_name.get()
        player_1_pos = utils.LadderFile.get_position(player_1)
        player_2 = self.opponent_name.get()
        player_2_pos = utils.LadderFile.get_position(player_2)

        if not self.checkPositionIfWithinRange(player_1_pos, player_2_pos):
            self.alert_msg_2.set(
                "Opponent is not within position range (>0 , <= 3)")
            return

        if not self.checkChallengeDate():
            self.alert_msg_2.set("Challenge Date must be in the future")
            return

        if self.checkIfPlayerNotExists(player_1):
            self.alert_msg_2.set("Player does not exist!")
            return

        if self.checkIfPlayerNotExists(player_2):
            self.alert_msg_2.set("Opponent does not exist!")
            return

        match_date = datetime.strftime(
            self.dateentry_create_match.get_date(), "%d-%m-%Y"
        )

        utils.DataFile.create_match(
            player_1, player_1_pos, player_2, player_2_pos, match_date
        )
        print("match created")
        self.getUpcomingMatches()

    def goBack(self):
        self.page.destroy()
        pages.StartPage.MainMenu(self.root)

    def checkChallengeDate(self):
        return self.dateentry_create_match.get_date() >= datetime.now().date()

    # Check if challenged player is up to 3 positions higher than current player
    def checkPositionIfWithinRange(self, player_1_pos, player_2_pos):
        print(player_1_pos, player_2_pos)
        print(player_1_pos - player_2_pos <=
              3 and player_1_pos - player_2_pos > 0)
        return player_1_pos - player_2_pos <= 3 and player_1_pos - player_2_pos > 0

    def checkIfPlayerExists(self, player_name):
        return player_name in self.ladder_data

    def checkIfPlayerNotExists(self, player_name):
        return player_name not in self.ladder_data

    def checkIfCorrectNameFormat(self, player_name):
        x = player_name.split(" ")
        print(x)
        if len(x) == 2:
            if x[0] == "" or x[1] == "":
                return False
            else:
                return True
        else:
            return False

    def checkIfCorrectScoreFormat(self, score):
        x = score.split("-")
        print(x)
        if len(x) == 2:
            if x[0] == "" or x[1] == "":
                return False
            else:
                try:
                    int(x[0])
                    int(x[1])
                    return True
                except TypeError:
                    return False
        else:
            return False

    # Function to add player to the ladder
    def register(self):

        player_name = self.player_name.get()

        if self.checkIfPlayerExists(player_name):
            self.alert_msg_1.set("Player already exists!")
        elif not self.checkIfCorrectNameFormat(player_name):
            self.alert_msg_1.set(
                "Player Name should be <First Name> <Last Name>")
        else:
            utils.DataFile.add_player(
                player_name, datetime.now().strftime("%d-%m-%Y"))
            utils.LadderFile.add_player(player_name)
            self.alert_msg_1.set(f"Player {player_name} added!")

        self.ladder_data = utils.LadderFile.get_ladder()

    # Function to withdraw player from the ladder
    def withdraw(self):

        player_name = self.player_name.get()

        if self.checkIfPlayerNotExists(player_name):
            self.alert_msg_1.set("Player does not exist!")
        else:
            utils.DataFile.remove_player(
                player_name,
                utils.LadderFile.get_position(player_name),
                datetime.now().strftime("%d-%m-%Y"),
            )
            utils.LadderFile.remove_player(player_name)
            self.alert_msg_1.set(f"Player {player_name} removed!")

        self.ladder_data = utils.LadderFile.get_ladder()
