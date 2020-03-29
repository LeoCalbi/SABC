'''
Simplex Artificial Bee Colony algorithm
'''


import argparse
import time

import numpy as np

import abeec
from abeec import abc_cli_parser, abc_algorithm
from amoeba import amoeba_cli_parser, simplex_coordinates, downhill_simplex
from utils import ListAction, FUNCTIONS, print_statistics


def renew_food_sources(food_sources, trails, limit, lower_bounds, upper_bounds, function, *args):
    '''
    Scout bees stage
    '''
    n_food_sources, n_vars = food_sources.shape
    assert(n_food_sources == trails.size)

    for i, trail in enumerate(trails):
        if trail >= limit:
            simplex = simplex_coordinates(food_sources[i])
            food_sources[i], _ = downhill_simplex(
                simplex, function, *args
            )
            trails[i] = 0
            if not np.array_equal(food_sources[i], abeec.find_best(food_sources, function)):
                food_sources[i] = abeec.renew_food_source(
                    food_sources[i], lower_bounds, upper_bounds
                )
    return food_sources


def sabc_cli_parser():
    '''
    Create a standard input arguments parser
    '''
    parser = argparse.ArgumentParser(
        prog='sabeec', description='Simplex Artificial Bee Colony algorithm'
    )
    abc_group = parser.add_argument_group('ABC params')
    amoeba_group = parser.add_argument_group('Nelder-Mead params')
    abc_group.add_argument(
        dest='n_food_sources', action='store', default=100,
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
        '-l', '--limit', action='store', default=20,
        type=int, help='trails limit'
    )
    abc_group.add_argument(
        '--abc_iterations', action='store', default=3000,
        type=int, help='maximum number of iterations'
    ),
    abc_group.add_argument(
        '-c', '--abc_stop', action='store', default=100,
        type=int, help='maximum number of non-changing best value before stopping'
    ),
    amoeba_group.add_argument(
        '--nm_iterations', action='store', default=3000,
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
    parser.add_argument(
        '-r', '--runtimes', action='store', default=1,
        type=int, help='number of executions'
    )
    return parser


def main():
    parser = sabc_cli_parser()
    args = parser.parse_args()
    abeec.renew_food_sources = renew_food_sources
    results = []
    mins = []
    iterations = []
    times = []
    for _ in range(args.runtimes):
        start_time = time.time()
        result, n_iteration = abc_algorithm(
            args.n_food_sources, args.lower_bounds, args.upper_bounds,
            args.limit, args.abc_stop, args.abc_iterations, FUNCTIONS[args.function],
            args.nm_iterations, args.tol, args.alpha, args.beta, args.gamma
        )
        times.append(time.time() - start_time)
        results.append(result)
        iterations.append(n_iteration)
        mins.append(FUNCTIONS[args.function](result))

    # Print results
    if args.runtimes == 1:
        print(f'Result: {results[0]}')
        print(f'Minimum: {mins[0]}')
        print(f'Iterations: {iterations[0]}/{args.abc_iterations}')
        print(f'Execution time: {times[0]} seconds')
    else:
        print_statistics(results, mins, iterations, args.abc_iterations, FUNCTIONS[args.function])
        print(f'Mean execution time: {np.mean(times)} seconds')
        print(f'Total execution time: {np.sum(times)} seconds')


if __name__ == "__main__":
    main()
