class View:

    @staticmethod
    def prompt_for_tournament():
        tournament = dict()
        tournament['name'] = input("Name: ")
        tournament['place'] = input("Place: ")
        tournament['date_begin'] = input("Begin date: ")
        tournament['date_end'] = input("End date: ")
        tournament['tournament_type'] = input("Type: ")
        tournament['description'] = input("Description: ")
        tournament['nb_tours'] = int(input("Number of rounds: "))
        # todo gestion des erreurs
        return tournament

    @staticmethod
    def prompt_for_nb_of_players():
        nb_players = int(input("Number of players: "))
        # todo gestion des erreurs
        return nb_players

    @staticmethod
    def prompt_for_player():
        player = dict()
        player['firstname'] = input("Player lastname: ")
        player['lastname'] = input("Player firstname: ")
        player['birthdate'] = input("Birthdate: ")
        player['gender'] = input("Gender: ")
        player['rank'] = input("Rank: ")
        # todo gestion des erreurs
        return player

    @staticmethod
    def prompt_for_tour():
        tour = dict()
        tour['name'] = input("Tour name: ")
        tour['date_begin'] = input("Begin date: ")
        tour['date_end'] = input("End date: ")
        return tour

    @staticmethod
    def prompt_for_scores(tour, match):
        print('scores du tour ' + tour, 'match ' + str(match))
        scores = dict()
        scores['player_1'] = float(input("Score player 1: "))
        scores['player_2'] = float(input("Score player 2: "))
        return scores

    @staticmethod
    def print_matches(tour):
        print(f"Matches tour {tour.tour_id}")
        for v in tour.matches.values():
            print(f"Scores match {v.match_id:<5} p{v.id_player_1}: {v.score_match_player_1:3} / "
                  f"p{v.id_player_2}: {v.score_match_player_2:3}")

    @staticmethod
    def print_infos_players(players):
        # todo trier par score décroissant
        print('\nInfos joueurs')
        for v in players.values():
            print(f"Id: {v.player_id:<2} | {v.firstname:>12} {v.lastname:12} | Score: {v.score:2}")
        print('\n')
