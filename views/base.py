from datetime import datetime
from views.validate_input import validate_user_input as vui


class View:

    @staticmethod
    def prompt_for_tournament():
        tournament = dict()
        tournament['name'] = input("Tournament name: ")
        tournament['place'] = input("Place: ")
        ask_date_begin = 1
        while ask_date_begin == 1:
            try:
                tournament['date_begin'] = vui("Begin date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
                # check if the date is correct
                datetime.strptime(tournament['date_begin'], '%d-%m-%Y %H:%M:%S')
                ask_date_begin = 0
            except ValueError:
                ask_date_begin = 1
                print("Incorrect date")
        tournament['tournament_type'] = vui("Type ('Blitz', 'Bullet', 'Coup rapide'): ", type_=str.lower, range_=('blitz', 'bullet', 'coup rapide'))
        tournament['description'] = input("Description: ")
        tournament['nb_tours'] = vui("Number of rounds: ", int, min_=1)
        return tournament

    @staticmethod
    def prompt_for_nb_of_players(tournament_name):
        nb_players = vui(f"Number of players for tournament \"{tournament_name}\": ", int, range_=(range(2, 1000, 2)))
        return nb_players

    @staticmethod
    def prompt_for_player(player_id):
        player = dict()
        player['lastname'] = input(f"Player {player_id} lastname: ")
        player['firstname'] = input(f"Player {player_id} firstname: ")
        ask_birthdate = 1
        while ask_birthdate == 1:
            try:
                player['birthdate'] = vui(f"Player {player_id} birthdate (dd-mm-yyyy) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4}')
                # check if the date is correct
                datetime.strptime(player['birthdate'], '%d-%m-%Y')
                ask_birthdate = 0
            except ValueError:
                print("Incorrect date string")
                ask_birthdate = 1
        player['gender'] = vui(f"Player {player_id} gender (F/M/N): ", type_=str.lower, range_=('f', 'm', 'n'))
        player['rank'] = vui(f"Player {player_id} rank: ", type_=float, min_=0)
        return player

    @staticmethod
    def prompt_for_tour():
        print('Create new tour')
        tour = dict()
        try:
            tour['date_begin'] = vui("Begin date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(tour['date_begin'], '%d-%m-%Y %H:%M:%S')
        except ValueError:
            print("Incorrect date string")
        return tour

    @staticmethod
    def prompt_for_scores(tour, match, id_player_1, id_player_2, name_player_1, name_player_2):
        print('Enter scores of tour ' + str(tour), 'match ' + str(match))
        scores = dict()
        check = 0
        while check != 1:
            scores['player_1'] = vui(f"Score player 1: id {id_player_1} - name {name_player_1}: ", type_=float, range_=(0, 0.5, 1))
            scores['player_2'] = vui(f"Score player 2: id {id_player_2} - name {name_player_2}: ", type_=float, range_=(0, 0.5, 1))
            check = scores['player_1'] + scores['player_2']
        return scores

    @staticmethod
    def prompt_for_end_date(tour_or_tournament):
        date_end = None
        try:
            date_end = vui(f"{tour_or_tournament} end date (dd-mm-yyyy hh:mm:ss) : ", type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(date_end, '%d-%m-%Y %H:%M:%S')
        except ValueError:
            print("Incorrect date string")
        return date_end

    @staticmethod
    def prompt_update_scores():
        ans = vui("Update scores (y/n)? ", type_=str.lower, range_=('y', 'n'))
        return True if ans == 'y' else False

    @staticmethod
    def print_message(message):
        print(message)

    @staticmethod
    def print_matches(tour):
        print(f"Matches tour {tour.tour_id}")
        for v in tour.matches.values():
            print(f"Scores match {v.match_id:<5} player id {v.id_player_1}: {v.score_match_player_1:3} / "
                  f"player id {v.id_player_2}: {v.score_match_player_2:3}")

    @staticmethod
    def print_tour(tour):
        active = 'active' if tour.active else 'over'
        print(f"[Tour {tour.tour_id}: {active}]")

    @staticmethod
    def print_infos_players(players):
        # todo trier par score décroissant
        print('\nPlayers information')
        for v in players.values():
            print(f"Id: {v.player_id:<2} | {v.firstname:>12} {v.lastname:12} | Score: {v.score:2}")
        print('\n')

    @staticmethod
    def menu():
        print('[1] Create tournament')
        print('[2] Add player to current tournament')
        print('[3] Create round / update scores')
        print('[4] Update players rank')
        print('[5] Display report')
        print('[0] Exit')

        option = vui("Choose option: ", type_=float, range_=(range(0, 5)))
        return option
