"""Define the main controller."""
from models import models
from create_pairs import create_first_tour_pairs, create_tour_pairs


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

    def maj_scores(self, tour):
        for i in range(len(tour.matches)):
            s = self.view.prompt_for_scores(tour.name, tour.matches[i+1].match_id)
            score_match_player_1 = s['player_1']
            score_match_player_2 = s['player_2']
            # Update match scores
            tour.matches[i+1].score_match_player_1 = score_match_player_1
            tour.matches[i+1].score_match_player_2 = score_match_player_2
            # Update players score
            id_player_1 = tour.matches[i+1].id_player_1
            id_player_2 = tour.matches[i+1].id_player_2
            self.tournament.players[id_player_1].score += score_match_player_1
            self.tournament.players[id_player_2].score += score_match_player_2

        # Print infos match
        self.view.print_matches(tour)

        # Print infos players
        self.view.print_infos_players(self.tournament.players)

    def add_players(self):
        nb_of_players = self.view.prompt_for_nb_of_players()
        for i in range(nb_of_players):
            # todo : id will be PK with autoincrement in bdd
            p = self.view.prompt_for_player()
            self.tournament.add_player(i + 1,
                                       p['firstname'],
                                       p['lastname'],
                                       p['birthdate'],
                                       p['gender'],
                                       p['rank'])

    def run(self):
        # update instance of empty Tournament that has been created in __init__
        self.create_tournament()
        self.add_players()

        for i in range(self.tournament.nb_tours):
            tour = self.create_tour_and_matches()
            self.maj_scores(tour)
