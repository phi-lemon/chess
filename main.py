"""Entry point."""
from models.tournament import Tournament
from controllers.base import Controller
from views.base import View


def main():

    tournament = Tournament()
    view = View()

    # Create tournament
    c = Controller(tournament, view)
    c.run()


if __name__ == "__main__":
    main()
