from datetime import datetime


class DataFile:

    data_list = []
    file_name = "data.txt"

    @classmethod
    def read_data_file(cls):
        _data_list = []
        with open(cls.file_name, "r") as f:  # Open file for read
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
                    date = datetime.strptime(line[1], "%d-%m-%Y")
                elif line[0] == "-":
                    action = "remove"
                    line = line.split("/")
                    name_1 = line[0][1:]
                    name_split = name_1.split(" ")
                    name_1 = name_split[0] + " " + name_split[1]
                    position_1 = name_split[2]
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
    def write_data_file_from_data_list(cls):
        _data_list = cls.data_list
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


DataFile.read_data_file()
print(DataFile.data_list)
DataFile.write_data_file_from_data_list()
