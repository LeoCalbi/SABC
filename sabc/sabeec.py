'''
Simplex Artificial Bee Colony algorithm
'''


import argparse

import numpy as np

import abeec
from abeec import abc_cli_parser, abc_algorithm
from amoeba import amoeba_cli_parser, simplex_coordinates, downhill_simplex
from utils import *


def renew_food_sources(food_sources, trails, limit, lower_bounds, upper_bounds, *args):
    '''
    Scout bees stage
    '''
    n_food_sources, n_vars = food_sources.shape
    assert(n_food_sources == trails.size)

    for i, trail in enumerate(trails):
        if trail >= limit:
            simplex = simplex_coordinates(food_sources[i])
            food_sources[i], _ = downhill_simplex(
                simplex, *args
            )
    return food_sources


def sabc_cli_parser():
    '''
    Create a standard input arguments parser
    '''
    parser = argparse.ArgumentParser(
        prog='sabc', description='Simplex Artificial Bee Colony algorithm'
    )
    abc_group = parser.add_argument_group('ABC params')
    amoeba_group = parser.add_argument_group('Nelder-Mead params')
    abc_group.add_argument(
        dest='n_food_sources', action='store', default=10,
        type=int, help='number of food sources'
    )
    abc_group.add_argument(
        dest='lower_bounds', action=ListAction,
        help='lower bounds for each variable',
    )
    abc_group.add_argument(
        dest='upper_bounds', action=ListAction,
        help='upper bounds for each variable',
    )
    abc_group.add_argument(
        '-l', '--limit', action='store', default=50,
        type=int, help='trails limit'
    )
    abc_group.add_argument(
        '--abc_iterations', action='store', default=1000,
        type=int, help='maximum number of iterations'
    ),
    amoeba_group.add_argument(
        '--nm_iterations', action='store', default=1000,
        type=int, help='maximum number of iterations'
    ),
    amoeba_group.add_argument(
        '-t', '--tol', action='store', default=1e-5,
        type=float, help='tolerance for the stopping criteria'
    ),
    amoeba_group.add_argument(
        '-a', '--alpha', action='store', default=1,
        type=float, help='coefficient for reflection'
    ),
    amoeba_group.add_argument(
        '-b', '--beta', action='store', default=0.5,
        type=float, help='coefficient for contraction'
    ),
    amoeba_group.add_argument(
        '-g', '--gamma', action='store', default=2,
        type=float, help='coefficient for expansion'
    )
    parser.add_argument(
        '-f', '--function', action='store', default='rosenbrock',
        type=str, choices=FUNCTIONS.keys(), help='benchmark function'
    )
    return parser


def main():
    parser = sabc_cli_parser()
    args = parser.parse_args()
    abeec.renew_food_sources = renew_food_sources
    minimum = abc_algorithm(
        args.n_food_sources, args.lower_bounds, args.upper_bounds,
        args.limit, args.abc_iterations, FUNCTIONS[args.function],
        args.nm_iterations, args.tol, args.alpha, args.beta, args.gamma
    )
    print(f'Result: {minimum}')


if __name__ == "__main__":
    main()
