from tinydb import where
import models.db as db


class Player:

    def __init__(self, player_id, firstname, lastname, birthdate, gender, rank, tournament):
        self.player_id = player_id
        self.tournament = tournament
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.gender = gender
        self.__rank = rank
        self.__score = 0

        # save instance attributes to db, without tournament object
        db.serialize(db.TABLE_PLAYERS, vars(self), 'tournament')

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
        db.TABLE_PLAYERS.update({'_Player__score': score}, where('player_id') == self.player_id)

