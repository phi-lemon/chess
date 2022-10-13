"""Main controller."""
from models.tour import Tour
from models.player import Player
from controllers.create_pairs import create_first_tour_pairs, create_tour_pairs


class Controller:
    def __init__(self, tournament, view):
        self.tournament = tournament
        self.view = view

    def create_tournament(self):
        tournament_params = self.view.prompt_for_tournament()
        self.tournament.add_tournament(
            tournament_params['name'],
            tournament_params['place'],
            tournament_params['date_begin'],
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
        tour = Tour()
        t = self.view.prompt_for_tour()
        tour.add_tour(t['date_begin'], None, self.tournament)
        self.view.print_message(f"Tour {tour.tour_id} created\n")
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
        # tour.matches is a dict but stored in db as a list
        for i in range(len(tour.matches)):
            id_player_1 = tour.matches[i+1].id_player_1
            id_player_2 = tour.matches[i+1].id_player_2
            name_player_1 = tour.tournament.players[id_player_1].lastname
            name_player_2 = tour.tournament.players[id_player_2].lastname
            s = self.view.prompt_for_scores(
                tour.tour_id,
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

        # End of round
        date_end = self.view.prompt_for_end_date('Tour')
        tour.stop(date_end)

        # Print infos players
        self.view.print_infos_players(self.tournament.players)
        # End of tournament
        if len(self.tournament.table_tours) == self.tournament.nb_tours:
            date_end = self.view.prompt_for_end_date('Tournament')
            self.tournament.stop(date_end)

    # def add_players(self):
    #     # get nb of players already registered
    #     nb_players = Player.get_players_nb(self.tournament)
    #     player_id = nb_players + 1
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
                   {'id': 8, 'firstname': 'Dee Dee', 'lastname': 'Bridgewater',
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
                # Create tournament
                # Is there an active tournament?
                if self.tournament.deserialize_active_tournament():
                    self.view.print_message("A tournament is already active.")
                else:
                    self.create_tournament()
            elif menu == 2:
                # do not add players if a round is already created
                # todo create function
                if len(self.tournament.table_tours) > 0:
                    self.view.print_message(
                        "You can't add player after a round has been created")
                # add players to an active tournament
                elif self.tournament.deserialize_active_tournament():
                    self.add_players()
                else:
                    self.view.print_message("Create a tournament is required before adding players.")
            elif menu == 3:
                # Create round or update score
                # Need players
                if Player.get_players_nb(self.tournament) == 0:
                    self.view.print_message("Please add players first.")
                # Need even number of players
                elif Player.get_players_nb(self.tournament) % 2 != 0:
                    self.view.print_message(
                        "Number of player must be even. Add a player.")
                else:
                    # Deserialize tournament, players and tours
                    if not self.tournament.name:
                        self.tournament = self.tournament.deserialize_active_tournament()
                    self.tournament.deserialize_players()
                    for serialized_tour in self.tournament.table_tours:
                        tour = self.tournament.deserialize_tour(serialized_tour)
                        self.view.print_tour(tour)
                    if len(self.tournament.tours) == 0:
                        self.create_tour_and_matches()
                    else:
                        last_tour = self.tournament.tours[-1]
                        if last_tour.is_active_tour():
                            if self.view.prompt_update_scores():
                                last_tour.deserialize_matches()
                                self.maj_scores(last_tour)
                        else:
                            # if len(self.tournament.tours) < self.tournament.nb_tours:
                            if len(self.tournament.table_tours) < self.tournament.nb_tours:
                                self.create_tour_and_matches()

            menu = self.view.menu()

    def run(self):
        self.actions()
