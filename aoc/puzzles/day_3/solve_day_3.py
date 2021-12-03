import copy
import os
from collections import Counter
from pathlib import Path

from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE

os.environ['LOG_LEVEL'] = 'DEBUG'
from aoc import logger
from aoc.utils import input_loader


def solve(day, sample):
    logger.info(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    bin_numbers = list_input

    numbers2 = copy.copy(bin_numbers)
    gamma_rate = calc_rate(bin_numbers)
    epsilon_rate = calc_rate(bin_numbers, type='eps')
    print("GAMMA:", gamma_rate)
    print("EPS", epsilon_rate)

    eps_value = to_int(epsilon_rate)
    gam_val = to_int(gamma_rate)

    logger.info(f'eps {eps_value}')
    logger.info(f'{gam_val=}')
    answer = eps_value * gam_val
    logger.info(f"The answer is {answer}\n")


    oxy_rate = to_int(calc_rate2(copy.copy(numbers2)))
    co2_rate = to_int(calc_rate2(copy.copy(numbers2), type='co2'))

    logger.info(f'{oxy_rate=}')
    logger.info(f'{co2_rate=}')

    logger.info(f'{life_support(oxy_rate, co2_rate)=}')


def co2_rating():
    # least common
    # if equal keep 0
    pass

def life_support(ox, co2):
    return ox * co2

def to_int(bits):
    value = 0
    for i, bit in enumerate(reversed(bits)):
        value += bit*2**(i)
    return value


def calc_rate2(numbers, type='oxy'):

    consider_bit = 0
    while len(numbers) > 1:
        bit_count = [0 for i in range(len(numbers[0]))]
        lines = len(numbers)

        for number in numbers:
            for i, bit in enumerate(number):
                if bit == '1':
                    bit_count[i] += 1

        if type == 'oxy':
            keep_number = int(bit_count[consider_bit] >= lines - bit_count[consider_bit])
        else:
            keep_number = (bit_count[consider_bit] < lines - bit_count[consider_bit])

        numbers = list(filter(lambda x: int(x[consider_bit]) == int(keep_number), numbers))
        consider_bit += 1

    numbers = list(map(int, numbers[0]))
    return [0,0,0] + numbers


def calc_rate(numbers, type='gamma'):
    bit_count = [0 for i in range(len(numbers[0]))]
    lines = len(numbers)

    for number in numbers:
        for i, bit in enumerate(number):
            if bit == '1':
                bit_count[i] += 1

    if type=='gamma':
        result = list(map(lambda x: 1 if x >= lines //2 else 0, bit_count))
    else:
        result = list(map(lambda x: 1 if x < lines //2 else 0, bit_count))

    return [0,0,0] + result

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    # solve(_day_num, sample=False)
    solve(_day_num, sample=True)
