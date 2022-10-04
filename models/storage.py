from tinydb import TinyDB


class SaveToDb:
    db = TinyDB('data.json', indent=4)
    table_tournaments = db.table("Tournaments")
    table_players = db.table("Players")
    table_tours = db.table("Tours")
    table_matches = db.table("Matches")

    @staticmethod
    def save(table, attr, *exclude_attr):
        """
        Serialize instance attributes in a dict and insert in db
        :param table: table in which save data
        :param attr: dict - ex. : vars(self)
        :param exclude_attr: attributes not to be inserted (ex. instance object)
        :return: None
        """
        if exclude_attr:
            dict_from_attr = {k: v for k, v in attr.items() if k not in exclude_attr}
        else:
            dict_from_attr = {k: v for k, v in attr.items()}
        table.insert(dict_from_attr)
