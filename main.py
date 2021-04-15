import tkinter.font as tkFont
# to compare datetime for editing the results of future matches
from datetime import datetime

# Import tkinter (the different functions)
from tkinter import (
    Button,
    Canvas,
    Entry,
    Frame,
    Grid,
    Label,
    LabelFrame,
    Menu,
    StringVar,
    Tk,
    messagebox,
    ttk,
)

from tkcalendar import Calendar, DateEntry  # download tkcalendar

# Data File Helper


class DataFile:

    data_list = []
    file_name = "data.txt"

    @classmethod  # class method decorator: https://www.geeksforgeeks.org/classmethod-in-python/
    def read_data_file(cls):
        _data_list = []
        with open(cls.file_name, "r") as f:  # Open file for read
            for line in f.readlines():  # Read line-by-line
                line = line.strip()  # Removes any spaces before or after the string

                if line == "":
                    return

                # Keep a single data in a dictionary
                data = {}
                action = ""  # + - empty etc
                name_1 = ""
                name_2 = ""
                position_1 = ""
                position_2 = ""
                date = ""
                results = []

                # Check if line represents results (), new player (+) or remove player(-)
                if line[0] == "+":
                    action = "add"
                    line = line.split("/")
                    name_1 = line[0][1:]  # removing the + in the list

                    # Convert to Datetime object
                    date = datetime.strptime(line[1], "%d-%m-%Y")
                elif line[0] == "-":
                    action = "remove"
                    line = line.split("/")
                    name_1 = line[0][1:]
                    name_split = name_1.split(" ")
                    name_1 = name_split[0] + " " + name_split[1]
                    position_1 = name_split[2]

                    # Convert to Datetime object
                    date = datetime.strptime(line[1], "%d-%m-%Y")
                else:
                    action = "result"
                    line = line.split("/")

                    name_1 = line[0]
                    name_split = name_1.split(" ")
                    name_1 = name_split[0] + " " + name_split[1]
                    position_1 = name_split[2]

                    name_2 = line[1]
                    name_split = name_2.split(" ")
                    name_2 = name_split[0] + " " + name_split[1]
                    position_2 = name_split[2]

                    # Convert to Datetime object
                    date = datetime.strptime(line[2], "%d-%m-%Y")

                    results = line[3].split(" ")
                    if results[0] == "":
                        results = []

                data["action"] = action
                data["name_1"] = name_1
                data["name_2"] = name_2
                data["position_1"] = position_1
                data["position_2"] = position_2
                data["date"] = date
                data["results"] = results

                _data_list.append(data)

        cls.data_list = _data_list

    @classmethod
    def write_data_file(cls, data):
        with open(cls.file_name, "w") as f:  # Open file for write
            for x in data:
                f.write(str(x) + "\n")

    @classmethod
    def write_data_file_from_data_list(cls, data_list=[]):

        if data_list == []:
            _data_list = cls.data_list
        else:
            _data_list = data_list

        with open(cls.file_name, "w") as f:  # Open file for write
            for x in _data_list:
                if x["action"] == "result":
                    f.write(
                        f"{x['name_1']} {x['position_1']}/{x['name_2']} {x['position_2']}/{datetime.strftime(x['date'], '%d-%m-%Y')}/{' '.join(x['results'])} \n"
                    )
                elif x["action"] == "add":
                    f.write(
                        f"+{x['name_1']}/{datetime.strftime(x['date'], '%d-%m-%Y')}"
                        + "\n"
                    )
                elif x["action"] == "remove":
                    f.write(
                        f"-{x['name_1']} {x['position_1']}/{datetime.strftime(x['date'], '%d-%m-%Y')}"
                        + "\n"
                    )
                else:
                    print("error")

    @classmethod
    def create_match(cls, name_1, pos_1, name_2, pos_2, date):
        cls.append(f"{name_1} {pos_1}/{name_2} {pos_2}/{date}/")

    @classmethod
    def append(cls, line):
        with open(cls.file_name, "a") as f:  # Open file for write
            f.write(str(line) + "\n")

    @classmethod
    def add_player(cls, player_name, join_date):
        cls.append(f"+{str(player_name)}/{str(join_date)}")

    @classmethod
    def remove_player(cls, player_name, position, leave_date):
        cls.append(f"-{str(player_name)} {str(position)}/{str(leave_date)}")

    @classmethod
    def get_data(cls):
        cls.read_data_file()
        return cls.data_list


# -------------------- Ladder File Helper --------------------


class LadderFile:

    ladder = []
    historical_ladder = []
    file_name = "ladder.txt"

    @classmethod
    def read_ladder_file(cls):
        _ladder = []
        with open(cls.file_name, "r") as f:  # Open file for read
            for line in f:  # Read line-by-line
                line = line.strip()

                if line == "":
                    return

                _ladder.append(line)

        cls.ladder = _ladder

    @classmethod
    def get_ladder(cls):
        cls.read_ladder_file()
        return cls.ladder

    @classmethod
    def get_historical_ladder(cls, search_date):
        match_data = DataFile.get_data()
        cls.historical_ladder = cls.get_ladder()
        n = len(match_data) - 1

        while match_data[n]["date"].date() >= search_date:

            player_1 = match_data[n]["name_1"]

            player_2 = match_data[n]["name_2"]

            results = match_data[n]["results"]
            if match_data[n]["action"] == "result":
                pos_1 = int(match_data[n]["position_1"]) - 1
                pos_2 = int(match_data[n]["position_2"]) - 1
                if determine_winner(match_data[n]["results"]) == 0:
                    winner = player_1
                else:
                    winner = player_2

                if player_1 == winner:
                    cls.reverse_update_position(player_1, pos_1, player_2)

            elif match_data[n]["action"] == "add":
                print(f"reverse add player {player_1}")
                cls.reverse_add_player(player_1)

            elif match_data[n]["action"] == "remove":
                pos_1 = int(match_data[n]["position_1"]) - 1
                print(f"reverse remove player {player_1}")
                cls.reverse_remove_player(player_1, pos_1)
            n -= 1  # go up 1 line

        return cls.historical_ladder

    @classmethod
    def reverse_update_position(cls, player_1, pos_1, player_2):
        player_1_position = cls.historical_ladder.index(player_1)  # Winner
        player_2_position = cls.historical_ladder.index(player_2)  # Loser
        # No update if player 1 (winner) is already in a higher position
        if player_1_position < player_2_position:
            return

        # Revert back to original pos
        cls.historical_ladder.pop(cls.historical_ladder.index(player_1))
        cls.historical_ladder.insert(pos_1, player_1)
        return

    @classmethod
    def reverse_add_player(cls, player_name):
        pos = cls.historical_ladder.index(player_name)
        cls.historical_ladder.pop(pos)

    @classmethod
    def reverse_remove_player(cls, player_name, pos):
        cls.historical_ladder.insert(pos, player_name)

    @classmethod
    def write_ladder(cls, ladder_list):
        with open(cls.file_name, "w") as f:  # Open file for write
            for x in ladder_list:
                f.write(str(x) + "\n")

    @classmethod
    def update_position(cls, player_1, player_2):
        # Updates player_1 position with player_2's position

        player_1_position = cls.ladder.index(player_1)  # Winner
        player_2_position = cls.ladder.index(player_2)  # Loser

        # No update if player 1 (winner) is already in a higher position
        if player_1_position < player_2_position:
            return

        # remove player 1 name from current position and insert player 1's name into 1 position above player 2
        cls.ladder.insert(
            cls.ladder.index(player_2), cls.ladder.pop(
                cls.ladder.index(player_1))
        )
        cls.write_ladder(cls.ladder)
        return

    @classmethod
    def add_player(cls, player_name):
        cls.ladder.append(player_name)
        cls.write_ladder(cls.ladder)

    @classmethod
    def remove_player(cls, player_name):
        cls.ladder.pop(cls.ladder.index(player_name))
        cls.write_ladder(cls.ladder)

    @classmethod
    def get_position(cls, player_name):
        cls.get_ladder()
        return cls.ladder.index(player_name) + 1


# -------------------- Helper Functions --------------------


def set_window_center(window, width, height):

    w_s = window.winfo_screenwidth()
    h_s = window.winfo_screenheight()

    x_co = (w_s - width) / 2
    y_co = (h_s - height) / 2 - 50
    window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
    window.minsize(width, height)


def get_screen_size(window):

    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):

    return window.winfo_reqwidth(), window.winfo_reqheight()


def treeview_sort_column(tv, col, reverse):

    l = [(tv.set(k, col), k) for k in tv.get_children("")]

    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def determine_winner(matches):

    player_1_games = 0
    player_2_games = 0

    if len(matches) < 2:
        return "TBA"

    for match in matches:
        if match != '':
            match = match.split("-")
            if match[0] > match[1]:
                player_1_games += 1
            else:
                player_2_games += 1

    if player_1_games > player_2_games:
        return 0
    else:
        return 1


def update_position(ladder: [], player_1, player_2):
    # Updates player_1 position with player_2's position

    player_1_position = ladder.index(player_1)  # Winner
    player_2_position = ladder.index(player_2)  # Loser

    # No update if player 1 (winner) is already in a higher position
    if player_1_position < player_2_position:
        return ladder

    ladder.insert(ladder.index(player_2), ladder.pop(ladder.index(player_1)))
    return ladder


# Calculates matches played by player
def calculate_matches_played(data):
    output = {}
    for x in data:
        print(x)
        if x["action"] == "result":
            if x["name_1"] not in output:
                output[x["name_1"]] = 1
            else:
                output[x["name_1"]] += 1
            if x["name_2"] not in output:
                output[x["name_2"]] = 1
            else:
                output[x["name_2"]] += 1
    return output


# Main Menu Screen
class MainMenu:
    def __init__(self, master=None):  # to store the 'master page'

        self.root = master  # to store the 'root' window
        self.root.title("Main Menu")
        # position the window in centre of screen
        set_window_center(self.root, 300, 180)
        self.init_page()  # to call on the next function

    def init_page(self):

        self.page = Frame(self.root)  # create frame for new page
        self.page.pack(pady=10)  # position 10 units vertical from the frame

        fontStyle = tkFont.Font(family="Lucida Grande", size=16)
        Label(self.page, text="Badminton Ladder Main Menu", font=fontStyle).grid(
            row=0, column=0
        )  # position the title 'invisible table'

        # button format and position
        button_viewer = Button(self.page, text="Viewer", command=self.goViewer)
        button_viewer.grid(row=1, column=0, stick="NSEW", pady=8)
        button_player = Button(self.page, text="Player", command=self.goPlayer)
        button_player.grid(row=2, column=0, stick="NSEW", pady=8)

    def goViewer(self):  # when click the viewer destroy the current page
        self.page.destroy()
        Viewer(self.root)  # loads the viewer page

    def goPlayer(self):
        self.page.destroy()
        Player(self.root)


# Viewer Screen

class Viewer:  # making class of functions for viewer
    def __init__(self, master=None):  # settle the data and build the components

        self.root = master
        self.root.title("Badminton Ladder")
        self.w = 800  # width and height of whole screen, 'golden ratio'
        self.h = 600
        set_window_center(self.root, self.w, self.h)

        # Load Data from txt files
        # getting ladder data from ladder file (another class)
        self.ladder_data = LadderFile.get_ladder()
        # getting match data from data file (another class)
        self.match_data = DataFile.get_data()
        # function that finds highest and lowest (dictionary)
        self.matches_played = calculate_matches_played(self.match_data)

        # tkinter class to input variable texts (for the input of position)
        self.var_position = StringVar()
        self.var_name = StringVar()  # for input/output to display name
        self.results_1 = StringVar()  # display results of most active or least active players

        self.name_filter = StringVar()
        self.name_filter.set("Input Name")

        self.init_ladder()
        self.init_page()

    def init_ladder(self):

        self.left_frame = Frame(self.root)  # defining the frame for ladder
        # left side for both ladder and data
        self.left_frame.pack(side="left", anchor="w")

        # back Button
        Button(self.left_frame, text="<<< Back", command=self.goBack, bg="red").pack(
            side="top", fill="both"
        )

        # Tree View
        self.ladder = ttk.Treeview(
            self.left_frame, show="headings", height=600)
        self.ladder.pack(side="left")  # better way to arrange the components

        # Column Names formatting the ladder
        self.ladder["columns"] = ("#", "Name")

        self.ladder.column("#", width=25)
        self.ladder.column("Name", width=175)

        self.ladder.heading("#", text="#")
        self.ladder.heading("Name", text="Name")

        self.resetTreeView(self.ladder)  # clear existing data on ladder
        # Load Ladder Data take already loaded data and insert into tree view
        self.loadLadderData()

        # when clicking on name will update player info
        self.ladder.bind("<<TreeviewSelect>>", self.displayData)

    def goBack(self):  # called when press back button

        self.footer_frame.destroy()  # destroy current page, frames
        self.body_frame.destroy()
        self.head_frame.destroy()
        self.ladder.destroy()
        self.left_frame.destroy()
        MainMenu(self.root)  # go back to main menu after clicking back

    # Load ladder data into tree view function used above ^
    def loadLadderData(self):

        # 'enumerate helps get the index and name in the list
        for pos, name in enumerate(self.ladder_data):
            self.ladder.insert(
                "",
                "end",  # insert data to the end of the list
                text="",
                values=(pos + 1, name),  # add 1 for the index
            )

    # Load historical ladder data into tree view
    def loadHistoricalLadderData(self, historical_ladder):
        self.resetTreeView(self.ladder)  # clear current tree first
        for pos, name in enumerate(historical_ladder):  # same as previous
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
        # calling on variable 'var_position' to output name and position
        Label(self.head_frame, textvariable=self.var_position).pack(anchor="w")
        # Name
        Label(self.head_frame, textvariable=self.var_name).pack(anchor="w")

        # ----- Body Frame -----
        # User options
        self.body_frame = LabelFrame(self.right_frame, text="Options")
        self.body_frame.pack(fill="both", expand="yes")

        # Most Active Player Button
        button_most_active_player = Button(
            self.body_frame, text="Most Active Player", command=self.getMostActivePlayer
        )
        # 'Ew' expands the button to 'maximise'
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

        # Historical Leaderboard Input (date)
        self.date_entry = DateEntry(
            self.body_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/mm/y",
        )
        self.date_entry.grid(row=2, column=1, padx=(
            10, 100))  # spacing the date

        # Footer Frame (bottom)
        # All challenges (All button)
        self.footer_frame = Frame(self.right_frame)
        self.footer_frame.pack(fill="both")

        button_all_matches = Button(
            self.footer_frame, text="All", command=self.getAllMatches
        )
        button_all_matches.grid(row=0, column=0, sticky="W")
        # Upcoming Challenges
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

        # Tree View (bottom right)
        self.upcoming_challenges = ttk.Treeview(
            self.footer_frame, show="headings")
        self.upcoming_challenges.grid(column=0, row=1, columnspan=7)

        # Column Names for tree view
        self.upcoming_challenges["columns"] = (
            "Match Date",
            "Player 1",
            "Player 2",
            "Match 1",
            "Match 2",
            "Match 3",
            "Winner",
        )

        self.upcoming_challenges.column(
            "Match Date", width=100)  # defines the width
        self.upcoming_challenges.column("Player 1", width=90)
        self.upcoming_challenges.column("Player 2", width=90)
        self.upcoming_challenges.column("Match 1", width=70)
        self.upcoming_challenges.column("Match 2", width=70)
        self.upcoming_challenges.column("Match 3", width=70)
        self.upcoming_challenges.column("Winner", width=98)

        self.upcoming_challenges.heading(
            "Match Date", text="Match Date")  # defines the text
        self.upcoming_challenges.heading("Player 1", text="Player 1")
        self.upcoming_challenges.heading("Player 2", text="Player 2")
        self.upcoming_challenges.heading("Match 1", text="Match 1")
        self.upcoming_challenges.heading("Match 2", text="Match 2")
        self.upcoming_challenges.heading("Match 3", text="Match 3")
        self.upcoming_challenges.heading("Winner", text="Winner")

    def getAllMatches(self):  # when you press All button it calls this function
        self.resetTreeView(self.upcoming_challenges)
        for data in self.match_data:
            if data["action"] == "result":

                results = {}
                results[0] = "-"
                results[1] = "-"
                results[2] = "-"
                winner = determine_winner(data["results"])

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

                    results = {}
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"
                    winner = determine_winner(data["results"])
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

    def resetTreeView(self, tree):  # empty current tree to display new match results
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

                    results = {}
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"
                    winner = determine_winner(data["results"])
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
                    results = {}
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"

                    winner = determine_winner(data["results"])
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
        historical_ladder = LadderFile.get_historical_ladder(selected_date)
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
            f"Most Active Players: {str(', '.join(most_active_player))} ({max_matches_played} matche(s))"
        )

    def getLeastActivePlayer(self):
        min_matches_played = min(self.matches_played.values())
        least_active_player = [
            name
            for (name, total_matches) in self.matches_played.items()
            if total_matches == min_matches_played
        ]
        self.results_1.set(
            f"Least Active Players: {str(', '.join(least_active_player))} ({min_matches_played} matche(s))"
        )


# -------------------- Player Screen --------------------


class Player:
    def __init__(self, master=None):

        self.root = master
        self.root.title("Badminton Ladder")
        self.w = 800
        self.h = 600
        set_window_center(self.root, self.w, self.h)

        # Load Data from txt files
        self.ladder_data = LadderFile.get_ladder()
        self.match_data = DataFile.get_data()
        self.matches_played = calculate_matches_played(self.match_data)
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
        ):
            if self.match_already_won_at_game_2(game_1_score, game_2_score, game_3_score):

                results = [game_1_score, game_2_score, game_3_score]
                self.match_data[idx]["results"] = results
                DataFile.write_data_file_from_data_list(self.match_data)
                self.updateLadder()
                self.getUpcomingMatches()
                self.alert_msg_3.set("Score Updated!")

        else:
            # self.alert_msg_3.set("Invalid Format, use <int>-<int>")
            pass

    def match_already_won_at_game_2(self, game_1_score, game_2_score, game_3_score):

        g1_p1 = game_1_score.split("-")[0]
        g1_p2 = game_1_score.split("-")[1]
        g2_p1 = game_2_score.split("-")[0]
        g2_p2 = game_2_score.split("-")[1]

        if (g1_p1 > g1_p2 and g2_p2 > g2_p1) or (g1_p2 > g1_p1 and g2_p1 > g2_p2):
            if game_3_score == "":
                self.alert_msg_3.set("Game 3 score missing")
                return False
            return self.checkIfCorrectScoreFormat(game_3_score)
        else:
            if game_3_score != "":
                self.alert_msg_3.set("Game 3 should be empty")
                return False
            return True

    def updateLadder(self):
        winner = determine_winner(
            self.match_data[self.selected_item_id]["results"])
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
            LadderFile.update_position(
                self.selection_player_1, self.selection_player_2)

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

        self.match_data = DataFile.get_data()
        self.resetTreeView(self.upcoming_challenges)

        for idx, data in enumerate(self.match_data):
            if data["date"] >= datetime.now() or data["results"] == []:
                if data["action"] == "result":
                    # Default Dictionary that returns '-' if key error
                    results = {}
                    results[0] = "-"
                    results[1] = "-"
                    results[2] = "-"
                    winner = determine_winner(data["results"])
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
        player_1_pos = LadderFile.get_position(player_1)
        player_2 = self.opponent_name.get()
        player_2_pos = LadderFile.get_position(player_2)

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

        DataFile.create_match(
            player_1, player_1_pos, player_2, player_2_pos, match_date
        )
        print("match created")
        self.getUpcomingMatches()

    def goBack(self):
        self.page.destroy()
        MainMenu(self.root)

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
                    s1 = int(x[0])
                    s2 = int(x[1])

                    if (s1 >= 20 and s2 >= 20) and abs(s1-s2) != 2:
                        self.alert_msg_3.set(
                            "Tie Score Margin != 2")
                        return False

                    if (s1 < 20 and s2 < 20):
                        self.alert_msg_3.set("score_1 < 20 and score_2 < 20")
                        return False

                    return True
                except:
                    self.alert_msg_3.set("Invalid Format, use <int>-<int>")
                    return False
        else:
            return False

    # Function to add player to the ladder
    def register(self):

        player_name = self.player_name.get()

        # player should not be added if already
        if self.checkIfPlayerExists(player_name):
            self.alert_msg_1.set("Player already exists!")
        # to prevent the programme from crashing when there is new players
        elif not self.checkIfCorrectNameFormat(player_name):
            self.alert_msg_1.set(
                "Player Name should be <First Name> <Last Name>")

        else:
            DataFile.add_player(
                player_name, datetime.now().strftime("%d-%m-%Y"))  # Format as dd-mm-yy https://www.programiz.com/python-programming/datetime/strftime
            LadderFile.add_player(player_name)
            self.alert_msg_1.set(f"Player {player_name} added!")

        self.ladder_data = LadderFile.get_ladder()

    # Function to withdraw player from the ladder
    def withdraw(self):

        player_name = self.player_name.get()

        if self.checkIfPlayerNotExists(player_name):
            self.alert_msg_1.set("Player does not exist!")
        else:
            DataFile.remove_player(
                player_name,
                LadderFile.get_position(player_name),
                datetime.now().strftime("%d-%m-%Y"),
            )
            LadderFile.remove_player(player_name)
            self.alert_msg_1.set(f"Player {player_name} removed!")

        self.ladder_data = LadderFile.get_ladder()


# Main App Class
class App(Tk):  # start tkinter, use class to hold the functions together

    def __init__(self):

        Tk.__init__(self)

        # main menu
        MainMenu(self)

        self.mainloop()  # loop to keep the app online


App()  # calling the class to run
