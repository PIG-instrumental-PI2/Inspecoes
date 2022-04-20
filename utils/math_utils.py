from typing import List

FLOAT_DECIMAIS = 4


def format_float(number):
    return round(number, FLOAT_DECIMAIS)


def avg(numbers: List):
    return round(
        sum(numbers) / len(numbers),
        FLOAT_DECIMAIS,
    )
