class View:
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


