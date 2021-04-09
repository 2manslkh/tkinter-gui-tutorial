from datetime import datetime


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

    l = [(tv.set(k, col), k) for k in tv.get_children('')]

    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(
        tv, col, not reverse))


def determine_winner(matches):

    player_1_games = 0
    player_2_games = 0

    if len(matches) < 2:
        return "TBA"

    for match in matches:
        match = match.split("-")
        if match[0] > match[1]:
            player_1_games += 1
        else:
            player_2_games += 1

    if player_1_games > player_2_games:
        return 0
    else:
        return 1


def update_position(ladder: [], player_1: str, player_2: str = "test"):
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
        if x['name_1'] not in output:
            output[x['name_1']] = 1
        else:
            output[x['name_1']] += 1
        if x['name_2'] not in output:
            output[x['name_2']] = 1
        else:
            output[x['name_2']] += 1
    return output


class DataFile:

    data_list = []
    file_name = "data.txt"

    @classmethod
    def read_data_file(cls):
        with open(cls.file_name, 'r') as f:  # Open file for read
            for line in f.readlines():  # Read line-by-line
                line = line.strip()

                if line == "":
                    return

                # Keep a single data in a dictionary
                data = {}
                action = ""
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
                    name_1 = line[0][1:]
                    date = datetime.strptime(line[1], '%d-%m-%Y')
                elif line[0] == "-":
                    action = "remove"
                    line = line.split("/")
                    name_1 = line[0][1:]
                    name_split = name_1.split(" ")
                    name_1 = name_split[0] + " " + name_split[1]
                    position = name_split[2]
                    date = datetime.strptime(line[1], '%d-%m-%Y')
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

                    date = datetime.strptime(line[2], '%d-%m-%Y')

                    results = line[3].split(" ")
                    if results[0] == '':
                        results = []

                data["action"] = action
                data["name_1"] = name_1
                data["name_2"] = name_2
                data["position_1"] = position_1
                data["position_2"] = position_2
                data["date"] = date
                data["results"] = results

                cls.data_list.append(data)

    @classmethod
    def write_data_file(cls, data):
        with open(file_name, 'w') as f:  # Open file for write
            for x in data:
                f.write(x + "\n")

    @classmethod
    def append(cls, line):
        with open(file_name, 'a') as f:  # Open file for write
            f.write(line + "\n")

    @classmethod
    def add_player(cls, player_name, join_date):
        with open(file_name, 'a') as f:  # Open file for write
            f.write(f"+{player_name}/{join_date}")

    @classmethod
    def remove_player(cls, player_name, position, leave_date):
        with open(file_name, 'a') as f:  # Open file for write
            f.write(f"-{player_name} {position}/{leave_date}")

    @classmethod
    def get_data(cls):
        cls.read_data_file()
        return cls.data_list


class LadderFile:

    ladder = []
    file_name = "ladder.txt"

    @classmethod
    def read_ladder_file(cls):
        with open(cls.file_name, 'r') as f:  # Open file for read
            for line in f:  # Read line-by-line
                line = line.strip()

                if line == "":
                    return

                cls.ladder.append(line)

    @classmethod
    def get_ladder(cls):
        cls.read_ladder_file()
        return cls.ladder

    @classmethod
    def write_ladder(cls, ladder_list):
        with open(cls.file_name, 'w') as f:  # Open file for write
            for x in ladder_list:
                f.write(x + "\n")

    @classmethod
    def update_position(cls, player_1: str, player_2: str = "test"):
        # Updates player_1 position with player_2's position

        player_1_position = cls.ladder.index(player_1)  # Winner
        player_2_position = cls.ladder.index(player_2)  # Loser

        # No update if player 1 (winner) is already in a higher position
        if player_1_position < player_2_position:
            print(cls.ladder)
            return

        cls.ladder.insert(cls.ladder.index(player_2),
                          cls.ladder.pop(cls.ladder.index(player_1)))
        cls.write_ladder(cls.ladder)
        print(cls.ladder)
        return

    @classmethod
    def add_player(cls, player_name):
        cls.ladder.append(player_name)
        cls.write_ladder(cls.ladder)
        print(cls.ladder)

    @classmethod
    def remove_player(cls, player_name):
        cls.ladder.pop(cls.ladder.index(player_name))
        cls.write_ladder(cls.ladder)
        print(cls.ladder)
