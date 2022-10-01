# Create pairs of players for tour #1
def create_first_tour_pairs(players):
    """
    Creates a list of players pairs for the first tour
    :param players: list of all tournament players (can't be odd)
    :return: list: [(,), (,), (,), (,)]
    """
    # Number of players must be even
    if len(players) % 2 != 0:
        raise RuntimeError("Number of players can't be odd")

    # Creating list of tuples (player_id, player_rank)
    players_ranked = []
    for p in players.values():
        players_ranked.append((p.player_id, p.rank))
    # Sort list by rank (asc)
    players_ranked.sort(key=lambda x: x[1])  # in-place
    # keep only player_id, sorted by rank
    players_ranked = [t[0] for t in players_ranked]

    # Making pairs of players
    mid_index = len(players_ranked) // 2
    group1 = players_ranked[:mid_index]
    group2 = players_ranked[mid_index:]

    pairs_of_players = list(zip(group1, group2))
    return pairs_of_players


# Create pairs of players for tours > #1
def create_tour_pairs(players):
    """
    Creates a list of players pairs
    :param players: list of all tournament players (can't be odd)
    :return: list: [(,), (,), (,), (,)]
    """
    # Number of players must be even
    if len(players) % 2 != 0:
        raise RuntimeError("Number of players can't be odd")

    # Creating list of tuples (player_id, player_score, player_rank)
    players_sorted_by_score = []
    for p in players.values():
        players_sorted_by_score.append((p.player_id, p.score, p.rank))
    # Sort list by score (asc)
    players_sorted_by_score.sort(key=lambda x: x[1])  # in-place
    # sort by rank if score is same
    players_sorted = []
    i = 0
    while i < len(players_sorted_by_score):
        players_sorted.append(players_sorted_by_score[i])
        # compare scores
        if players_sorted_by_score[i][1] == players_sorted_by_score[i - 1][1]:
            # compare ranks
            if players_sorted_by_score[i][2] < players_sorted_by_score[i - 1][2]:
                players_sorted.insert(
                    i - 1,
                    players_sorted_by_score[i]
                )
                players_sorted.pop()
        i += 1

    # keep only player_id
    players_sorted = [t[0] for t in players_sorted]

    # Making pairs of players
    pairs_of_players = []
    for i in range(int(len(players_sorted) / 2)):
        a, b = players_sorted.pop(), players_sorted.pop()
        pairs_of_players.append((a, b))

    return pairs_of_players
