"""Entry point."""

from models import models
from controllers.base import Controller
from views.base import View


def main():
    # deck = Deck()
    # view = View()
    # game = Controller(deck, view)
    # game.run()

    tournament = models.Tournament("super tournoi",
                                   "Nantes",
                                   '19-09-22 13:55:26',
                                   '19-09-22 13:55:26',
                                   'Blitz',
                                   ''
                                   )

    view = View()

    # Create tournament
    chess_tournament = Controller(tournament, view)


if __name__ == "__main__":
    main()