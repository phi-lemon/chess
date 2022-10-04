from datetime import datetime
from views.validate_input import validate_user_input as vui


class View:

    @staticmethod
    def prompt_for_tournament():
        tournament = dict()
        tournament['name'] = input("Name: ")
        tournament['place'] = input("Place: ")
        ask_date_begin, ask_date_end = 1, 1
        while ask_date_begin == 1:
            try:
                tournament['date_begin'] = vui("Begin date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
                # check if the date is correct
                datetime.strptime(tournament['date_begin'], '%d-%m-%Y %H:%M:%S')
                ask_date_begin = 0
            except ValueError:
                ask_date_begin = 1
                print("Incorrect date")
        while ask_date_end == 1:
            try:
                tournament['date_end'] = vui("End date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
                # check if the date is correct
                datetime.strptime(tournament['date_end'], '%d-%m-%Y %H:%M:%S')
                ask_date_end = 0
            except ValueError:
                ask_date_end = 1
                print("Incorrect date")
        tournament['tournament_type'] = vui("Type ('Blitz', 'Bullet', 'Coup rapide'): ", type_=str.lower, range_=('blitz', 'bullet', 'coup rapide'))
        tournament['description'] = input("Description: ")
        tournament['nb_tours'] = vui("Number of rounds: ", int, min_=1)
        return tournament

    @staticmethod
    def prompt_for_nb_of_players():
        nb_players = vui("Number of players: ", int, range_=(range(2, 1000, 2)))
        return nb_players

    @staticmethod
    def prompt_for_player():
        player = dict()
        player['firstname'] = input("Player lastname: ")
        player['lastname'] = input("Player firstname: ")
        ask_birthdate = 1
        while ask_birthdate == 1:
            try:
                player['birthdate'] = vui("Birthdate (dd-mm-yyyy) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4}')
                # check if the date is correct
                datetime.strptime(player['birthdate'], '%d-%m-%Y')
                ask_birthdate = 0
            except ValueError:
                print("Incorrect date string")
                ask_birthdate = 1
        player['gender'] = vui("Gender (F/M/N): ", type_=str.lower, range_=('f', 'm', 'n'))
        player['rank'] = vui("Rank: ", type_=float, min_=0)
        return player

    @staticmethod
    def prompt_for_tour():
        tour = dict()
        tour['name'] = input("Tour name: ")
        try:
            tour['date_begin'] = vui("Begin date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(tour['date_begin'], '%d-%m-%Y %H:%M:%S')
        except ValueError:
            print("Incorrect date string")
        try:
            tour['date_end'] = vui("End date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(tour['date_end'], '%d-%m-%Y %H:%M:%S')
        except ValueError:
            print("Incorrect date string")
        return tour

    @staticmethod
    def prompt_for_scores(tour, match):
        print('Entrer les scores du tour ' + tour, 'match ' + str(match))
        scores = dict()
        check = 0
        while check != 1:
            scores['player_1'] = vui("Score player 1 (0 / 0.5 / 1): ", type_=float, range_=(0, 0.5, 1))
            scores['player_2'] = vui("Score player 2 (0 / 0.5 / 1): ", type_=float, range_=(0, 0.5, 1))
            check = scores['player_1'] + scores['player_2']
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


# todo ajouter le numéro de joueur lors de l'ajout
# todo menu new tournament, add players (only before tournament is started), update ranks, reports

