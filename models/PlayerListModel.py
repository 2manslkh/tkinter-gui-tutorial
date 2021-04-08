class PlayerList():

    players = []
    num_players = 0

    def __init__(self, players):
        self.players = players
        self.num_players = len(players)

    # Returns player list
    def get_players(self):
        return self.players

    # Returns number of players
    def get_num_players(self):
        return self.num_players

    # Removes a player
    def remove_player(self, player_name):
        player_index = self.find_player_index(player_name)
        self.players.pop(player_index)
        self.num_players -= 1

    # Adds a player
    def add_player(self, player):
        self.players.append(player)
        self.num_players += 1

    # Edit a current player's position
    def edit_player_position(self, player_name, new_position):
        player_index = self.find_player_index(player_name)
        if player_index != -1:
            self.players[player_index].current_position = new_position

    # Find the player's index in the player list
    def find_player_index(self, player_name):
        i = 0
        for player in self.players:
            if player.name == player_name:
                return i
            else:
                i += 1
        # Return -1 if not found
        return -1

    # Get sorted list of players according to position
    def get_sorted_player_list(self):
        return self.players.sort(key=lambda x: x.position)
