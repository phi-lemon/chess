from pathlib import Path

# Create the data folder if it does not exist
data_path = Path.cwd() / 'data'
if not Path.exists(data_path):
    data_path.mkdir()


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
        dict_from_attr = {k: v for k, v in attr.items() if
                          k not in exclude_attr}
    else:
        dict_from_attr = {k: v for k, v in attr.items()}
    table.insert(dict_from_attr)
