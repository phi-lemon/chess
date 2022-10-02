"""Entry point."""

from models import models
from controllers.base import Controller
from views.base import View


def main():

    model = models.Tournament("super tournoi",
                              "Nantes",
                              '19-09-22 13:55:26',
                              '19-09-22 13:55:26',
                              'Blitz',
                              ''
                              )

    view = View()

    # Create tournament

    c = Controller(model, view)

    # todo créer une fonction run() dans le controller qui fait les actions ci-dessous
    c.add_players()
    #
    # # Tour 1 ######################################################################
    t1 = c.create_tour_and_matches()
    #
    # # Saisie des résultats du tour 1
    c.maj_scores(tour=t1)


if __name__ == "__main__":
    main()
