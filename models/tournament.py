import models.db as db
from models.player import Player


class Tournament:
    def __init__(self):
        """
        Intialize tournament with empty values. Use add_tournament to update instance
        """
        self.name = None
        self.place = None
        self.date_begin = None
        self.date_end = None
        self.nb_tours = 4
        self.tournament_type = None
        self.description = None
        self.players = {}
        self.tours = []
        self.matches_players = []
        self.active = 0

    def add_tournament(self, name, place, date_begin, tournament_type, description, nb_tours=4):
        """
        :param name:
        :param place:
        :param date_begin: '19/09/22 13:55:26'
        :param tournament_type:
        :param description:
        :param nb_tours:
        """
        self.name = name
        self.place = place
        self.date_begin = date_begin
        self.nb_tours = nb_tours
        self.tournament_type = tournament_type
        self.description = description
        self.players = {}
        self.tours = []
        self.active = 1

        # save instance attributes to db
        db.serialize(db.TABLE_TOURNAMENTS, vars(self))

    def stop(self, date_end):
        self.active = 0
        self.date_end = date_end
        # update tournament in db
        db.TABLE_TOURNAMENTS.update({'active': 0})
        db.TABLE_TOURNAMENTS.update({'date_end': date_end})

    def add_player(self, player_id, firstname, lastname, birthdate, gender, rank):
        self.players[player_id] = Player(player_id, firstname, lastname, birthdate, gender, rank, self)
        # todo add to tournament players in db

    def add_tour(self, tour):
        """
        add a tour to current tournament
        called by Tour().add_tour
        :param tour:
        :return:
        """
        self.tours.append(tour)
        # todo add to tournament tours in db


