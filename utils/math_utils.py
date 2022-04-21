from typing import List

FLOAT_DECIMAIS = 4


def format_float(number):
    return round(number, FLOAT_DECIMAIS)


def avg(numbers: List):
    return round(
        sum(numbers) / len(numbers),
        FLOAT_DECIMAIS,
    )


def cal_new_pos(initial_pos, begin_time_ms, final_time_ms, speed):
    """Calcula nova posicao do PIG baseando-se na leitura anterior e atual"""
    delta_time_secs = (final_time_ms - begin_time_ms) / 1000
    return initial_pos + speed * delta_time_secs
