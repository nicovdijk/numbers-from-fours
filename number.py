from typing import Dict, Optional

MAX_NUMBER_TO_SHOW = 50
MAX_NUMBER_TO_STORE = 100
MAX_NUMBER_OF_FOURS = 5


FORMULAS: Dict[int, str] = {}
NUMBER_OF_FOURS: Dict[int, int] = {}
NEW_FORMULAS: Dict[int, str] = {4: "4", 44: "44"}
NEW_NUMBER_OF_FOURS: Dict[int, int] = {4: 1, 44: 2}


def try_plus(number_1: int, number_2: int) -> None:
    try_add_number(number_1, "+", number_2, number_1 + number_2)


def try_minus(number_1: int, number_2: int) -> None:
    try_add_number(number_1, "-", number_2, number_1 - number_2)


def try_times(number_1: int, number_2: int) -> None:
    try_add_number(number_1, "*", number_2, number_1 * number_2)


def try_divide(number_1: int, number_2: int) -> None:
    if number_2 < 1e-9:
        return
    try_add_number(number_1, "/", number_2, number_1 / number_2)


def try_add_number(number_1, operation, number_2, new_number) -> None:
    if not is_valid_number(new_number):
        return
    new_integer = try_cast_to_integer(new_number)
    if new_integer is None:
        return
    new_number_of_fours = NUMBER_OF_FOURS[number_1] + NUMBER_OF_FOURS[number_2]
    if new_number_of_fours >= current_number_of_fours(new_integer):
        return
    formula = f"({FORMULAS[number_1]} {operation} {FORMULAS[number_2]})"
    # formula = f"({number_1} {operation} {number_2})"
    NEW_FORMULAS[new_integer] = formula
    NEW_NUMBER_OF_FOURS[new_integer] = new_number_of_fours


def current_number_of_fours(number: int) -> int:
    number_of_fours = NEW_NUMBER_OF_FOURS.get(number)
    if number_of_fours is None:
        number_of_fours = NUMBER_OF_FOURS.get(number)
    if number_of_fours is None:
        number_of_fours = MAX_NUMBER_OF_FOURS + 1
    return number_of_fours


def is_valid_number(number: float) -> bool:
    return 0 < number < MAX_NUMBER_TO_STORE


def try_cast_to_integer(number: float) -> Optional[int]:
    integer = int(number)
    return None if abs(integer - number) > 1e-9 else integer


def find_new_numbers(new_number: int) -> None:
    for number in FORMULAS:
        try_plus(new_number, number)
        try_minus(new_number, number)
        try_minus(number, new_number)
        try_times(new_number, number)
        try_divide(new_number, number)
        try_divide(number, new_number)


def get_next_number() -> int:
    min_number_of_fours = min(NEW_NUMBER_OF_FOURS.values())
    for number, number_of_fours in NEW_NUMBER_OF_FOURS.items():
        if number_of_fours == min_number_of_fours:
            return number
    raise Exception("This should not be possible!")


def main() -> None:
    while NEW_FORMULAS:
        new_number = get_next_number()
        FORMULAS[new_number] = NEW_FORMULAS.pop(new_number)
        NUMBER_OF_FOURS[new_number] = NEW_NUMBER_OF_FOURS.pop(new_number)
        find_new_numbers(new_number)
    print_formulas()


def print_formulas(new=False) -> None:
    formulas = NEW_FORMULAS if new else FORMULAS
    number_of_fours = NEW_NUMBER_OF_FOURS if new else NUMBER_OF_FOURS
    for number in range(1, MAX_NUMBER_TO_SHOW + 1):
        this_formula = formulas.get(number)
        if this_formula is None:
            this_formula = "X"
            this_number_of_fours = MAX_NUMBER_OF_FOURS
        else:
            this_number_of_fours = number_of_fours[number]
        fours = "fours" if this_number_of_fours > 1 else "four"
        print(f"{number:3} = {this_formula:40} ({this_number_of_fours} {fours})")


if __name__ == "__main__":
    main()
