from models.storage import SaveToDb
from models.player import Player


class Tournament:
    def __init__(self):
        """
        Intialize tournament with empty values. Use add_tournament_infos to update instance
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

    def add_tournament_infos(self, name, place, date_begin, date_end, tournament_type, description, nb_tours=4):
        """
        :param name:
        :param place:
        :param date_begin: '19/09/22 13:55:26'
        :param date_end:
        :param tournament_type:
        :param description:
        :param nb_tours:
        """
        self.name = name
        self.place = place
        self.date_begin = date_begin
        self.date_end = date_end
        self.nb_tours = nb_tours
        self.tournament_type = tournament_type
        self.description = description
        self.players = {}
        self.tours = []

        # save instance attributes to db
        SaveToDb.save(SaveToDb.table_tournaments, vars(self))

    def add_player(self, player_id, firstname, lastname, birthdate, gender, rank):
        self.players[player_id] = Player(player_id, firstname, lastname, birthdate, gender, rank, self)

    def add_tour(self, tour):
        self.tours.append(tour)
