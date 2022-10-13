import re
from rich.console import Console
from rich.text import Text

console = Console()


def validate_user_input(prompt, type_=None, min_=None, max_=None, range_=None,
                        regex=None):
    """
    check user input
    :param prompt: input text
    :param type_: type to check and convert to (int, str,...)
    :param min_: min value
    :param max_: max value
    :param range_: value must be in range.
    Pass tuple to check multiple values (ex. : ('a', 'b', 'c', 'd'))
    :param regex: value must match regex.
    Pass regex as a raw string : r'[A-Za-z0-9]+'
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
                msg = Text(f"Input type must be {type_.__name__}")
                msg.stylize("red")
                console.print(msg)
                continue
        if max_ is not None and ui > max_:
            msg = Text(f"Input must be less than or equal to {max_}")
            msg.stylize("red")
            console.print(msg)
        elif min_ is not None and ui < min_:
            msg = Text(f"Input must be greater than or equal to {min_}")
            msg.stylize("red")
            console.print(msg)
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                msg = Text(
                    f"Input must be between {range_.start} and {range_.stop}")
                msg.stylize("red")
                console.print(msg)
            else:
                if len(range_) == 1:
                    msg = Text("Input must be", *range_)
                    msg.stylize("red")
                    console.print(msg)
                else:
                    expected = " or ".join((", ".join(
                        str(x) for x in range_[:-1]), str(range_[-1])))
                    msg = Text(f"Input must be {expected}")
                    msg.stylize("red")
                    console.print(msg)
        elif regex is not None:
            check = re.compile(regex)
            if not re.fullmatch(check, ui):
                msg = Text(f"'{ui}' does not match required format")
                msg.stylize("red")
                console.print(msg)
            else:
                return ui
        else:
            return ui
