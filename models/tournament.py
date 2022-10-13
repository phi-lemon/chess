from models.player import Player
from models.tour import Tour
from tinydb import TinyDB, where
from models.serialize import serialize


class Tournament:
    TRN_LIST = TinyDB('data/tournaments_list.json', indent=4)

    def __init__(self, name=None, place=None, date_begin=None, date_end=None, nb_tours=None, tournament_type=None, description=None, active=0):
        """
        Intialize tournament with empty values. Use add_tournament to update instance
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
        self.matches_players = []
        self.active = active

        # each tournament has its own db
        self.tdb = TinyDB(
            'data/' + str(self.get_current_tournament_id()) + '.json',
            indent=4)
        self.table_tournaments = self.tdb.table("Tournaments")
        self.table_players = self.tdb.table("Players")
        self.table_tours = self.tdb.table("Tours")
        self.table_matches = self.tdb.table("Matches")

    @classmethod
    def get_current_tournament_id(cls):
        if not Tournament.TRN_LIST.search(where('active') == 1):
            return len(cls.TRN_LIST) + 1
        else:
            return 1 if len(cls.TRN_LIST) == 0 else len(cls.TRN_LIST)

    def add_tournament(self, name, place, date_begin, tournament_type, description, nb_tours=4):
        """
        Only one tournament may be active at a given time
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

        # self.tdb = TinyDB(
        #     'data/' + str(self.get_current_tournament_id() + 1) + '.json',
        #     indent=4)

        # add the tournament to tournaments_list db
        if Tournament.deserialize_active_tournament(self):
            raise RuntimeError("A tournament is already active")
        else:
            Tournament.TRN_LIST.insert({'active': 1})
            # save instance attributes (except db attributes)
            serialize(self.table_tournaments, vars(self), 'tdb', 'table_tournaments', 'table_players', 'table_tours', 'table_matches')

    def stop(self, date_end):
        self.active = 0
        self.date_end = date_end
        # update tournament in db
        self.table_tournaments.update({'active': 0})
        self.table_tournaments.update({'date_end': date_end})
        # update tournaments list
        Tournament.TRN_LIST.update({'active': 0}, where('active') == 1)
        # exit before create another tournament
        exit("End of tournament")

    def add_player(self, player_id, firstname, lastname, birthdate, gender, rank):
        self.players[player_id] = Player(player_id, firstname, lastname, birthdate, gender, rank, self)
        # save instance attributes to tournament db
        serialize(self.table_players, vars(self.players[player_id]), 'tournament', 'player_uid')
        # save instance attributes to players db
        serialize(Player.PLAYERS_LIST, vars(self.players[player_id]), 'player_id', 'tournament', 'score')

    def add_tour(self, tour):
        """
        add a tour to current tournament
        :param tour:
        :return:
        """
        self.tours.append(tour)
        # todo add to tournament tours in db

    def deserialize_active_tournament(self):
        """
        Check if there is an active tournament
        If no active instance, deserialize tournament to create one
        :return: if instance exists, return true else return instance.
        If no tournament is active return false
        """
        if Tournament.TRN_LIST.search(where('active') == 1):
            # is there an active instance?
            if self.name:
                return True
            # no active instance, deserialize to create one
            else:
                serialized_tournament = self.table_tournaments.all()[0]
                name = serialized_tournament['name']
                place = serialized_tournament['place']
                date_begin = serialized_tournament['date_begin']
                date_end = serialized_tournament['date_end']
                nb_tours = serialized_tournament['nb_tours']
                tournament_type = serialized_tournament['tournament_type']
                description = serialized_tournament['description']
                active = serialized_tournament['active']
                return Tournament(name, place, date_begin, date_end, nb_tours, tournament_type, description, active)
        else:
            return False

    def deserialize_players(self):
        for p in self.table_players:
            player_id = p['player_id']
            firstname = p['firstname']
            lastname = p['lastname']
            birthdate = p['birthdate']
            gender = p['gender']
            rank = p['_Player__rank']
            score = p['_Player__score']
            Player(player_id, firstname, lastname, birthdate, gender, rank, self, score)
            # Add players to tournament instance
            self.players[player_id] = Player(player_id, firstname, lastname, birthdate, gender, rank, self, score)

    def deserialize_tour(self, serialized_tour):
        tour_id = serialized_tour['tour_id']
        date_begin = serialized_tour['date_begin']
        date_end = serialized_tour['date_end']
        active = serialized_tour['active']
        tour = Tour(tour_id, self, date_begin, date_end, active)
        self.tours.append(Tour(tour_id, self, date_begin, date_end, active))
        return tour

    @staticmethod
    def is_active_tournament():
        return True if Tournament.TRN_LIST.search(where('active') == 1) else False

