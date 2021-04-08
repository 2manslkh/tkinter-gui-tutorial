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


ladder_list = ['V Axelsen',
               'L Chen',
               'TC Chou',
               'ZJ Lee',
               'YQ Shi',
               'K Momota',
               'KLA Ng',
               'A Antonsen',
               'D Lin',
               'AS Ginting',
               'K Tsuneyama',
               'KY Lee',
               'K Nishimoto',
               'J Christie',
               'TW Wang',
               'S Praneeth', 'Keng']

LadderFile.get_ladder()
LadderFile.write_ladder(ladder_list)
