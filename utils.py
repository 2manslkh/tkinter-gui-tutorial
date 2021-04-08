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

                    name_1 = line[0][1:]
                    name_split = name_1.split(" ")
                    name_1 = name_split[0] + " " + name_split[1]
                    position_1 = name_split[2]

                    name_2 = line[1][1:]
                    name_split = name_2.split(" ")
                    name_2 = name_split[0] + " " + name_split[1]
                    position_2 = name_split[2]

                    date = datetime.strptime(line[2], '%d-%m-%Y')

                    results = line[3].split(" ")

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
    def get_data(cls):
        cls.read_data_file()
        return cls.data_list


DataFile.get_data()


class LadderFile:

    ladder = []
    file_name = "ladder.txt"

    @classmethod
    def read_ladder_file(cls):
        with open(file_name, 'r') as f:  # Open file for read
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
    def write_ladder(cls):
        return cls.ladder
