from tinydb import where


class Match:
    def __init__(self, match_id, tour, id_player_1, id_player_2,
                 tournament_match_id):
        """
        A match is a tuple containing 2 lists [player, score]
        :param match_id:
        :param tour:
        :param id_player_1:
        :param id_player_1:
        """
        self.tour = tour
        self.tour_id = tour.tour_id
        self.match_id = match_id
        self.id_player_1 = id_player_1
        self.__score_match_player_1 = 0
        self.id_player_2 = id_player_2
        self.__score_match_player_2 = 0
        self.tournament_match_id = tournament_match_id

    @property
    def score_match_player_1(self):
        return self.__score_match_player_1

    @score_match_player_1.setter
    def score_match_player_1(self, score_match_player_1):
        if score_match_player_1 < 0:
            raise ValueError("Score must be positive")
        self.__score_match_player_1 = score_match_player_1

        # update match score in db
        self.tour.tournament.table_matches.update(
            {'_Match__score_match_player_1': score_match_player_1},
            where('tournament_match_id') == self.tournament_match_id)

    @property
    def score_match_player_2(self):
        return self.__score_match_player_2

    @score_match_player_2.setter
    def score_match_player_2(self, score_match_player_2):
        if score_match_player_2 < 0:
            raise ValueError("Score must be positive")
        self.__score_match_player_2 = score_match_player_2

        # update match score in db
        self.tour.tournament.table_matches.update(
            {'_Match__score_match_player_2': score_match_player_2},
            where('tournament_match_id') == self.tournament_match_id)
