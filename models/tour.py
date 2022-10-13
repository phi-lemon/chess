from tinydb import where
from models.match import Match
from models.serialize import serialize


class Tour:
    tour_id = 0

    def __init__(self, tour_id=0, tournament=None, date_begin=None,
                 date_end=None, active=0):
        self.tournament = tournament
        self.tour_id = tour_id
        self.date_begin = date_begin
        self.date_end = date_end
        self.matches = {}
        self.active = active

    def add_tour(self, date_begin, date_end, tournament):
        self.tournament = tournament
        # Tour.tour_id += 1
        self.tour_id = Tour.set_tour_id(self)
        self.date_begin = date_begin
        self.date_end = date_end
        self.active = 1

        # Can't create more tours than nb_tours defined in Tournament
        if self.tour_id > self.tournament.nb_tours:
            raise RuntimeError("Too much tours for this tournament")
        self.tournament.add_tour(self)

        # save instance attributes to db, without tournament object
        serialize(self.tournament.table_tours, vars(self), 'tournament')

    def set_tour_id(self):
        return len(self.tournament.table_tours) + 1

    def stop(self, date_end):
        self.active = 0
        self.date_end = date_end
        # update tour in db
        self.tournament.table_tours.update_multiple([
            ({'active': 0}, where('tour_id') == self.tour_id),
            ({'date_end': date_end}, where('tour_id') == self.tour_id),
        ])

    def is_active_tour(self):
        active_tour = self.tournament.table_tours.search(where('active') == 1)
        return True if active_tour else False

    @staticmethod
    def matches_to_list(item):
        return [i for i in item]

    def add_match(self, match_id, id_player_1, id_player_2,
                  tournament_match_id):
        """
        Creates a match and add it to tour's matches dict
        Method called from the controller
        :param match_id: match identifier for the round
        :param id_player_1:
        :param id_player_2:
        :param tournament_match_id: unique match identifier
        for the tournament
        :return:
        """
        self.matches[match_id] = Match(match_id, self, id_player_1,
                                       id_player_2, tournament_match_id)

        # append pair of players (set) to tournament
        self.tournament.matches_players.append({id_player_1, id_player_2})

        # save instance attributes to db, without tour object
        serialize(self.tournament.table_matches, vars(self.matches[match_id]),
                  'tour')
        # update tour matches
        self.tournament.table_tours.update(
            {'matches': self.matches_to_list(self.matches)})

    def deserialize_matches(self):
        """
        Deserialize matches of a tour
        :return: None
        """
        for m in self.tournament.table_matches:
            match_id = m['match_id']
            id_player_1 = m['id_player_1']
            id_player_2 = m['id_player_2']
            tournament_match_id = m['tournament_match_id']
            Match(match_id, self, id_player_1, id_player_2,
                  tournament_match_id)
            self.matches[match_id] = Match(match_id, self, id_player_1,
                                           id_player_2, tournament_match_id)
