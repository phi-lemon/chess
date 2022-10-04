from tinydb import TinyDB, where
db = TinyDB('data.json', indent=4)

table_tournaments = db.table("Tournaments")
table_players = db.table("Players")
table_tours = db.table("Tours")
table_matches = db.table("Matches")


class SaveToDb:

    @staticmethod
    def save(table, attr, *exclude_attr):
        """
        Serialize instance attributes in a dict and insert in db
        :param table: table in which save data
        :param attr: dict - ex. : vars(self)
        :param exclude_attr: attributes not to be inserted (ex. instance object)
        :return: None
        """
        if exclude_attr:
            dict_from_attr = {k: v for k, v in attr.items() if k not in exclude_attr}
        else:
            dict_from_attr = {k: v for k, v in attr.items()}
        table.insert(dict_from_attr)


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
        SaveToDb.save(table_tournaments, vars(self))

    def add_player(self, player_id, firstname, lastname, birthdate, gender, rank):
        self.players[player_id] = Player(player_id, firstname, lastname, birthdate, gender, rank, self)

    def add_tour(self, tour):
        self.tours.append(tour)


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
        SaveToDb.save(table_players, vars(self), 'tournament')

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
        table_players.update({'_Player__score': score}, where('player_id') == self.player_id)


class Tour:
    tour_id = 0

    def __init__(self, name, date_begin, date_end, tournament):
        self.tournament = tournament
        Tour.tour_id += 1
        self.tour_id = Tour.tour_id
        # Can't create more tours than nb_tours defined in Tournament
        if self.tour_id > self.tournament.nb_tours:
            raise RuntimeError("Too much tours for this tournament")

        self.name = name
        self.date_begin = date_begin  # todo à remplir automatiquement qd utilisateur crée le tour
        self.date_end = date_end  # todo à remplir automatiquement qd utilisateur marque tour comme terminé

        self.matches = {}

        # add this tour to tournament's list of tours
        self.tournament.add_tour(self)

        # save instance attributes to db, without tournament object
        SaveToDb.save(table_tours, vars(self), 'tournament')

    def add_match(self, match_id, id_player_1, id_player_2):
        """
        Creates a match and add it to tour's matches dict
        This method is called from the controller
        :param match_id:
        :param id_player_1:
        :param id_player_2:
        :return:
        """
        self.matches[match_id] = Match(match_id, self, id_player_1, id_player_2)


class Match:
    def __init__(self, match_id, tour, id_player_1, id_player_2):
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
        # instanciate a match
        self.match = ([self.id_player_1, self.__score_match_player_1], [self.id_player_2, self.__score_match_player_2])

        # save instance attributes to db, without tour object
        SaveToDb.save(table_matches, vars(self), 'tour', 'match')

    @property
    def score_match_player_1(self):
        return self.__score_match_player_1

    @score_match_player_1.setter
    def score_match_player_1(self, score_match_player_1):
        if score_match_player_1 < 0:
            raise ValueError("Score must be positive")
        self.__score_match_player_1 = score_match_player_1

        # update player score in db
        table_matches.update({'_Match__score_match_player_1': score_match_player_1}, where('match_id') == self.match_id)

    @property
    def score_match_player_2(self):
        return self.__score_match_player_2

    @score_match_player_2.setter
    def score_match_player_2(self, score_match_player_2):
        if score_match_player_2 < 0:
            raise ValueError("Score must be positive")
        self.__score_match_player_2 = score_match_player_2

        # update player score in db
        table_matches.update({'_Match__score_match_player_2': score_match_player_2}, where('match_id') == self.match_id)
