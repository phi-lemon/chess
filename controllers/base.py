"""Define the main controller."""
from models.tour import Tour
from controllers.create_pairs import create_first_tour_pairs, create_tour_pairs


class Controller:
    def __init__(self, tournament, view):
        self.tournament = tournament
        self.view = view

    def create_tournament(self):
        tournament_params = self.view.prompt_for_tournament()
        self.tournament.add_tournament_infos(
            tournament_params['name'],
            tournament_params['place'],
            tournament_params['date_begin'],
            tournament_params['date_end'],
            tournament_params['tournament_type'],
            tournament_params['description'],
            tournament_params['nb_tours']
            )

    def create_tour_and_matches(self):
        """
        Method that creates a tour, then creates pairs of players, then create matches for this tour
        For the first tour, player pairing is different
        :return:
        """
        t = self.view.prompt_for_tour()
        tour = Tour(t['name'], t['date_begin'], t['date_end'], self.tournament)
        if len(self.tournament.tours) == 1:
            players_tour = create_first_tour_pairs(self.tournament.players)
        else:
            players_tour = create_tour_pairs(self.tournament.players, self.tournament)

        self.create_matches(tour, players_tour)
        return tour

    def create_matches(self, tour, pairs_of_players):
        """
        Create matches and add them to current tour
        :param tour:
        :param pairs_of_players:
        :return:
        """
        match_id = 1
        tournament_match_id = len(self.tournament.matches_players)
        for pairs in pairs_of_players:
            tournament_match_id += 1
            id_player1, id_player2 = pairs
            tour.add_match(match_id, id_player1, id_player2, tournament_match_id)
            match_id += 1

    def maj_scores(self, tour):
        for i in range(len(tour.matches)):
            id_player_1 = tour.matches[i+1].id_player_1
            id_player_2 = tour.matches[i+1].id_player_2
            name_player_1 = tour.tournament.players[id_player_1].lastname
            name_player_2 = tour.tournament.players[id_player_2].lastname
            s = self.view.prompt_for_scores(
                tour.name,
                tour.matches[i + 1].match_id,
                id_player_1,
                id_player_2,
                name_player_1,
                name_player_2
            )
            score_match_player_1 = s['player_1']
            score_match_player_2 = s['player_2']
            # Update match scores
            tour.matches[i+1].score_match_player_1 = score_match_player_1
            tour.matches[i+1].score_match_player_2 = score_match_player_2
            # Update players score
            self.tournament.players[id_player_1].score += score_match_player_1
            self.tournament.players[id_player_2].score += score_match_player_2

        # Print infos players
        self.view.print_infos_players(self.tournament.players)

    # def add_players(self):
        # nb_of_players = self.view.prompt_for_nb_of_players(self.tournament.name)
        # for player_id in range(nb_of_players):
        #     player_id = player_id + 1
        #     p = self.view.prompt_for_player(player_id)
        #     self.tournament.add_player(player_id,
        #                                p['firstname'],
        #                                p['lastname'],
        #                                p['birthdate'],
        #                                p['gender'],
        #                                p['rank'])
    def add_players(self):
        players = [{'id': 1, 'firstname': 'Titi', 'lastname': 'Durand',
                    'birthdate': '07-05-76', 'gender': 'M', 'rank': 20},
                   {'id': 2, 'firstname': 'Mathilde', 'lastname': 'Dupont',
                    'birthdate': '04-07-95', 'gender': 'F', 'rank': 29},
                   {'id': 3, 'firstname': 'Gaston', 'lastname': 'Martin',
                    'birthdate': '04-07-95', 'gender': 'M', 'rank': 1},
                   {'id': 4, 'firstname': 'George', 'lastname': 'Harisson',
                    'birthdate': '04-07-95', 'gender': 'M', 'rank': 55},
                   {'id': 5, 'firstname': 'John', 'lastname': 'Lennon',
                    'birthdate': '04-07-95', 'gender': 'M', 'rank': 29},
                   {'id': 6, 'firstname': 'Alphonse', 'lastname': 'Daudet',
                    'birthdate': '04-07-95', 'gender': 'M', 'rank': 34},
                   {'id': 7, 'firstname': 'Ringo', 'lastname': 'Star',
                    'birthdate': '04-07-95', 'gender': 'M', 'rank': 76},
                   {'id': 8, 'firstname': 'Dee Dee',
                    'lastname': 'Bridgewater',
                    'birthdate': '04-07-95', 'gender': 'F', 'rank': 10}]

        for p in players:
            self.tournament.add_player(p['id'],
                                       p['firstname'],
                                       p['lastname'],
                                       p['birthdate'],
                                       p['gender'],
                                       p['rank'])

    def actions(self):
        menu = self.view.menu()
        while menu != 0:
            if menu == 1:
                self.create_tournament()
            elif menu == 2:
                self.add_players()
            elif menu == 3:
                for i in range(self.tournament.nb_tours):
                    tour = self.create_tour_and_matches()
                    self.maj_scores(tour)

            menu = self.view.menu()

    def run(self):
        self.actions()
