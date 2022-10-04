from models.storage import SaveToDb
from models.match import Match


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
        SaveToDb.save(SaveToDb.table_tours, vars(self), 'tournament')

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