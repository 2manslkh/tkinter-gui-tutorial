class Game():

    player_1_score = 0
    player_2_score = 0

    def __init__(self, raw_score_text):

        # parse raw score
        self.player_1_score, self.player_2_score = self.parse_raw_score(
            raw_score_text)

    def parse_raw_score(self, raw_score_text, split_char="-"):
        return raw_score_text.split(split_char)

    def get_player_1_score(self):
        return self.player_1_score

    def get_player_2_score(self):
        return self.player_2_score
