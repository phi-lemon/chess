import re


def validate_user_input(prompt, type_=None, min_=None, max_=None, range_=None, regex=None):
    """
    check user input
    :param prompt: input text
    :param type_: type to check and convert to (int, str,...)
    :param min_: min value
    :param max_: max value
    :param range_: value must be in range. Pass tuple to check multiple values (ex. : ('a', 'b', 'c', 'd'))
    :param regex: value must match regex. Pass regex as a raw string : r'[A-Za-z0-9]+'
    :return: validated input
    """
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print(f"Input type must be {type_.__name__}")
                continue
        if max_ is not None and ui > max_:
            print(f"Input must be less than or equal to {max_}")
        elif min_ is not None and ui < min_:
            print(f"Input must be greater than or equal to {min_}")
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                print(f"Input must be between {range_.start} and {range_.stop}")
            else:
                if len(range_) == 1:
                    print("Input must be", *range_)
                else:
                    expected = " or ".join((", ".join(str(x) for x in range_[:-1]), str(range_[-1])))
                    print(f"Input must be {expected}")
        elif regex is not None:
            check = re.compile(regex)
            if not re.fullmatch(check, ui):
                print(f"'{ui}' does not match required format")
            else:
                return ui
        else:
            return ui
