"""Define the main controller."""
from models import models
from views.base import View
from create_pairs import create_first_tour_pairs, create_tour_pairs


class Controller:
    def __init__(self, tournament, view):
        self.tournament = tournament
        self.view = view

    def create_tour_and_matches(self):
        """
        Method that creates a tour, then creates pairs of players, then create matches for this tour
        For the first tour, player pairing is different
        :return:
        """
        t = self.view.prompt_for_tour()
        tour = models.Tour(t['name'], t['date_begin'], t['date_end'], self.tournament)
        if len(self.tournament.tours) == 1:
            players_tour = create_first_tour_pairs(self.tournament.players)
        else:
            players_tour = create_tour_pairs(self.tournament.players)

        self.create_matches(tour, players_tour)
        return tour

    @staticmethod
    def create_matches(tour, pairs_of_players):
        """
        Create matches and add them to current tour
        :param tour:
        :param pairs_of_players:
        :return:
        """
        match_id = 1
        for pairs in pairs_of_players:
            id_player1, id_player2 = pairs
            tour.add_match(match_id, id_player1, id_player2)
            match_id += 1

    @staticmethod
    def print_matches(tour):
        print(f"Matches tour {tour.tour_id}")
        for v in tour.matches.values():
            print(f"Scores match {v.match_id:<5} p{v.id_player_1}: {v.score_match_player_1:3} / "
                  f"p{v.id_player_2}: {v.score_match_player_2:3}")

    def print_infos_joueurs(self):
        # todo trier par score décroissant
        print('\nInfos joueurs')
        for v in self.tournament.players.values():
            print(f"Id: {v.player_id:<2} | {v.firstname:>12} {v.lastname:12} | Score: {v.score:2}")
        print('\n')

    def maj_scores(self, tour):
        for i in range(len(tour.matches)):
            s = self.view.prompt_for_scores(tour.name, tour.matches[i+1].match_id)
            score_match_player_1 = s['player_1']
            score_match_player_2 = s['player_2']
            if score_match_player_1 + score_match_player_2 != 1:
                raise ValueError("Sum of players scores must be equal to 1")
            # Update match scores
            tour.matches[i+1].score_match_player_1 = score_match_player_1
            tour.matches[i+1].score_match_player_2 = score_match_player_2
            # Update players score
            id_player_1 = tour.matches[i+1].id_player_1
            id_player_2 = tour.matches[i+1].id_player_2
            self.tournament.players[id_player_1].score += score_match_player_1
            self.tournament.players[id_player_2].score += score_match_player_2

    def add_players(self):
        # for i in range(2):
        # todo : id will be PK with autoincrement in bdd

        #     p = self.view.prompt_for_player()
        #     self.tournament.add_player(i + 1,
        #                                p['firstname'],
        #                                p['lastname'],
        #                                p['birthdate'],
        #                                p['gender'],
        #                                p['rank'])
        players = [
            (1, 'Titi', 'Durand', '07-05-76', 'M', 20),
            (2, 'Mathilde', 'Dupont', '04-07-95', 'F', 29),
            (3, 'Gaston', 'Martin', '04-07-95', 'M', 1),
            (4, 'George', 'Harisson', '04-07-95', 'M', 55),
            (5, 'John', 'Lennon', '04-07-95', 'M', 8),
            (6, 'Alphonse', 'Daudet', '04-07-95', 'M', 34),
            (7, 'Ringo', 'Star', '04-07-95', 'M', 76),
            (8, 'Dee Dee', 'Bridgewater', '04-07-95', 'F', 10)
        ]
        for i in players:
            self.tournament.add_player(i[0],
                                       i[1],
                                       i[2],
                                       i[3],
                                       i[4],
                                       i[5]
                                       )


model = models.Tournament("super tournoi",
                          "Nantes",
                          '19-09-22 13:55:26',
                          '19-09-22 13:55:26',
                          'Blitz',
                          ''
                          )

c = Controller(model, View())
c.add_players()

# Tour 1 ######################################################################
t1 = c.create_tour_and_matches()

# Saisie des résultats du tour 1
c.maj_scores(tour=t1)


c.print_matches(t1)
c.print_infos_joueurs()


# Tour 2 ######################################################################
t2 = c.create_tour_and_matches()

# Saisie des résultats du tour 2
c.maj_scores(tour=t2)

c.print_matches(t2)
c.print_infos_joueurs()


# Tour 3 ######################################################################
t3 = c.create_tour_and_matches()

# Saisie des résultats du tour 2
c.maj_scores(tour=t3)

c.print_matches(t3)
c.print_infos_joueurs()


# Tour 4 ######################################################################
t4 = c.create_tour_and_matches()

# Saisie des résultats du tour 2
c.maj_scores(tour=t4)

c.print_matches(t4)
c.print_infos_joueurs()
