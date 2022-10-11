from tinydb import where
# import models.db as db
from models.serialize import serialize


class Player:

    def __init__(self, player_id, firstname, lastname, birthdate, gender, rank, tournament, score=0):
        self.player_id = player_id
        self.tournament = tournament
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.gender = gender
        self.__rank = rank
        self.__score = score

    @property
    def rank(self):
        return self.__rank

    @rank.setter
    def rank(self, rank):
        if rank < 0:
            raise ValueError("Rank must be a positive integer")
        self.__rank = rank

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score < 0:
            raise ValueError("Score must be positive")
        self.__score = score

        # update player score in db
        self.tournament.table_players.update({'_Player__score': score}, where('player_id') == self.player_id)

    @staticmethod
    def get_players_nb(tournament):
        if tournament.table_players:
            return len(tournament.table_players)
        else:
            return 0

