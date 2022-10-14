from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.table import Table
from views.validate_input import validate_user_input as vui


class View:
    console = Console()

    @staticmethod
    def prompt_for_tournament():
        tournament = dict()
        tournament['name'] = input("Tournament name: ")
        tournament['place'] = input("Place: ")
        ask_date_begin = 1
        while ask_date_begin == 1:
            try:
                tournament['date_begin'] = vui(
                    "Begin date (dd-mm-yyyy hh:mm:ss) : ", type_=str,
                    regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
                # check if the date is correct
                datetime.strptime(tournament['date_begin'],
                                  '%d-%m-%Y %H:%M:%S')
                ask_date_begin = 0
            except ValueError:
                ask_date_begin = 1
                msg = Text("Incorrect date")
                msg.stylize("red")
                View.console.print(msg)
        tournament['tournament_type'] = vui(
            "Type ('Blitz', 'Bullet', 'Coup rapide'): ", type_=str.lower,
            range_=('blitz', 'bullet', 'coup rapide'))
        tournament['description'] = input("Description: ")
        tournament['nb_tours'] = vui("Number of rounds: ", int, min_=1)
        return tournament

    @staticmethod
    def prompt_for_player(player_id):
        player = dict()
        player['lastname'] = input(f"Player {player_id} lastname: ")
        player['firstname'] = input(f"Player {player_id} firstname: ")
        ask_birthdate = 1
        while ask_birthdate == 1:
            try:
                player['birthdate'] = vui(
                    f"Player {player_id} birthdate (dd-mm-yyyy) : ", type_=str,
                    regex=r'\d{2}-\d{2}-\d{4}')
                # check if the date is correct
                datetime.strptime(player['birthdate'], '%d-%m-%Y')
                ask_birthdate = 0
            except ValueError:
                msg = Text("Incorrect date string")
                msg.stylize("red")
                View.console.print(msg)
                ask_birthdate = 1
        player['gender'] = vui(f"Player {player_id} gender (F/M/N): ",
                               type_=str.lower, range_=('f', 'm', 'n'))
        player['rank'] = vui(f"Player {player_id} rank: ", type_=float, min_=0)
        return player

    @staticmethod
    def prompt_for_tour():
        print('Create new tour')
        tour = dict()
        try:
            tour['date_begin'] = \
                vui("Begin date (dd-mm-yyyy hh:mm:ss) : ",
                    type_=str,
                    regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(tour['date_begin'], '%d-%m-%Y %H:%M:%S')
        except ValueError:
            msg = Text("Incorrect date string")
            msg.stylize("red")
            View.console.print(msg)
        return tour

    @staticmethod
    def prompt_for_scores(tour, match, id_player_1, id_player_2, name_player_1,
                          name_player_2):
        print('Enter scores of tour ' + str(tour), 'match ' + str(match))
        scores = dict()
        check = 0
        while check != 1:
            scores['player_1'] = vui(
                f"Score player 1: id {id_player_1} - name {name_player_1}: ",
                type_=float, range_=(0, 0.5, 1))
            scores['player_2'] = vui(
                f"Score player 2: id {id_player_2} - name {name_player_2}: ",
                type_=float, range_=(0, 0.5, 1))
            check = scores['player_1'] + scores['player_2']
        return scores

    @staticmethod
    def prompt_for_end_date(tour_or_tournament):
        date_end = None
        try:
            date_end = vui(
                f"{tour_or_tournament} end date (dd-mm-yyyy hh:mm:ss) : ",
                type_=str, regex=r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}')
            # check if the date is correct
            datetime.strptime(date_end, '%d-%m-%Y %H:%M:%S')
        except ValueError:
            msg = Text("Incorrect date string")
            msg.stylize("red")
            View.console.print(msg)
        return date_end

    @staticmethod
    def prompt_update_scores():
        ans = vui("Update scores (y/n)? ", type_=str.lower, range_=('y', 'n'))
        return True if ans == 'y' else False

    @staticmethod
    def print_message(message):
        msg = Text(message)
        msg.stylize("cyan")
        View.console.print(msg)

    @staticmethod
    def print_tour(tour):
        active = 'active' if tour.active else 'over'
        txt = Text(f"[Tour {tour.tour_id}: {active}]")
        txt.stylize("cyan")
        View.console.print(txt)

    @staticmethod
    def print_infos_players(players):
        # print('\nPlayers information')
        txt = Text("\nPlayers information\n")
        for v in players.values():
            txt += (
                f"Id: {v.player_id:<2} | {v.firstname:>12} {v.lastname:12} "
                f"| Score: {v.score:2}\n")
        txt += "\n"
        txt.stylize("cyan")
        View.console.print(txt)

    @staticmethod
    def prompt_for_player_uid():
        player_uid = vui("Enter player uid: ", type_=int, min_=1)
        return player_uid

    @staticmethod
    def prompt_for_player_rank(player_uid):
        player_rank = vui(f"Player {player_uid} rank: ", type_=float, min_=0)
        return player_rank

    @staticmethod
    def menu():
        txt_menu = Text(
            "\n"
            "[1] Create tournament\n"
            "[2] Add player to current tournament\n"
            "[3] Create round / update scores\n"
            "[4] Update players rank\n"
            "[5] Display reports\n"
            "[0] Exit\n"
        )
        txt_menu.stylize("green")
        View.console.print(txt_menu)

        option = vui("Choose option: ", type_=float, range_=(range(0, 6)))
        return option

    @staticmethod
    def menu_reports():
        txt_menu_report = Text(
            "\n"
            "[1] All players report\n"
            "[2] Tournaments report\n"
            "[3] Tournament's players report\n"
            "[4] Tournament's rounds report\n"
            "[5] Tournament's matches report\n"
            "[0] Exit reports\n"
        )
        txt_menu_report.stylize("sandy_brown")
        View.console.print(txt_menu_report)

        option = vui("Choose report: ", type_=float, range_=(range(0, 6)))
        return option

    @staticmethod
    def players_report(players):
        table = Table(title="List of players")
        table.add_column("Id", style="magenta")
        table.add_column("Firstname", style="cyan")
        table.add_column("Lastname", style="cyan")
        table.add_column("Birthdate", style="cyan")
        table.add_column("Gender", style="cyan")
        table.add_column("Rank", justify="right", style="cyan")
        for player in players:
            table.add_row(
                str(player['_Player__uid']),
                str(player['firstname']),
                str(player['lastname']),
                str(player['birthdate']),
                str(player['gender']),
                str(player['_Player__rank'])
            )
        print()
        View.console.print(table)

    @staticmethod
    def rounds_report(tnmt_id, rounds):
        table = Table(title=f"Tournament {tnmt_id}: List of rounds")
        table.add_column("Id", style="magenta")
        table.add_column("Begin date", style="cyan", no_wrap=True)
        table.add_column("End Date", style="cyan", no_wrap=True)
        table.add_column("Nb of matches", style="cyan")
        table.add_column("State", style="cyan")
        for round_ in rounds:
            table.add_row(
                str(round_['tour_id']),
                str(round_['date_begin']),
                str(round_['date_end']),
                str(len(round_['matches'])),
                "In progress" if str(round_['active']) == '1' else "Ended"
            )
        print()
        View.console.print(table)

    @staticmethod
    def matches_report(tnmt_id, matches):
        table = Table(title=f"Tournament {tnmt_id}: List of matches")
        table.add_column("Round Id", style="magenta")
        table.add_column("Player 1", style="cyan")
        table.add_column("Score player 1", style="cyan")
        table.add_column("Player 2", style="cyan")
        table.add_column("Score player 2", style="cyan")
        for match in matches:
            table.add_row(
                str(match['tour_id']),
                str(match['player_1_firstname']) + ' ' + str(
                    match['player_1_lastname']),
                str(match['_Match__score_match_player_1']),
                str(match['player_2_firstname']) + ' ' + str(
                    match['player_2_lastname']),
                str(match['_Match__score_match_player_2'])
            )
        print()
        View.console.print(table)

    @staticmethod
    def tournaments_report(tournaments):
        table = Table(title="List of tournaments")
        table.add_column("Name", style="magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Place", style="cyan")
        table.add_column("Begin date", style="cyan", no_wrap=True)
        table.add_column("End Date", style="cyan", no_wrap=True)
        table.add_column("Number of rounds", justify="right", style="cyan")
        table.add_column("Type", style="cyan")
        table.add_column("Description", style="cyan")
        table.add_column("State", style="cyan")
        for tournament in tournaments:
            table.add_row(
                str(tournament['id']),
                str(tournament['name']),
                str(tournament['place']),
                str(tournament['date_begin']),
                str(tournament['date_end']),
                str(tournament['nb_tours']),
                str(tournament['tournament_type']),
                str(tournament['description']),
                "In progress" if str(tournament['active']) == '1' else "Ended"
            )
        print()
        View.console.print(table)

    @staticmethod
    def prompt_report_sort_order():
        order = vui("Sort by rank ('y') or lastname (default)? ", type_=str.lower)
        return True if order == 'y' else False

    @staticmethod
    def prompt_report_tournament_id():
        tournament_id = vui("Tournament id: ", type_=int)
        return tournament_id
