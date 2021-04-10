class Player:

    name = ""
    wins = 0
    join_date = ""
    current_position = 0
    matches_played = 0
    current_opponent = ""

    def __init__(self, name, wins, join_date, current_position, matches_played):
        self.name = name
        self.wins = wins
        self.join_date = join_date
        self.current_position = current_position
        self.matches_played = matches_played
