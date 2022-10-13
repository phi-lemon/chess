from tinydb import TinyDB

tdb = TinyDB('data/data.json', indent=4)
TABLE_TOURNAMENTS = tdb.table("Tournaments")
TABLE_PLAYERS = tdb.table("Players")
TABLE_TOURS = tdb.table("Tours")
TABLE_MATCHES = tdb.table("Matches")


def serialize(table, attr, *exclude_attr):
    """
    Serialize instance attributes in a dict and insert in db
    :param table: table in which save data
    :param attr: dict - ex. : vars(self)
    :param exclude_attr: attributes not to be inserted
    (ex. instance object)
    :return: None
    """
    if exclude_attr:
        dict_from_attr = {k: v for k, v in attr.items()
                          if k not in exclude_attr}
    else:
        dict_from_attr = {k: v for k, v in attr.items()}
    table.insert(dict_from_attr)
