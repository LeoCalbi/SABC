'''
Artificial Bee Colony algorithm
'''


import argparse

import numpy as np

from utils import *


def gen_pop(n_food_sources, lower_bounds, upper_bounds):
    '''
    Generate the initial employed bees and food sources
    '''
    food_sources = np.full((n_food_sources, lower_bounds.size), lower_bounds)
    random_vars = np.random.random_sample(food_sources.shape)
    food_sources += random_vars * (upper_bounds - lower_bounds)
    return food_sources


def fitness(food_source, function):
    '''
    ABC fitness function
    '''
    value = function(food_source)
    return 1 / (1 + value) if value >= 0 else 1 + abs(value)


def new_food_source(food_sources, index):
    '''
    Employed/onlooker bees new food source discovery
    '''
    n_food_sources, n_vars = food_sources.shape
    d = np.random.choice(np.arange(n_vars))
    new_index = np.random.choice(
        np.delete(np.arange(n_food_sources), index)
    )
    food_source = np.array(food_sources[index], copy=True)
    food_source[d] += np.random.uniform(-1, 1) * (
        food_source[d] - food_sources[new_index][d]
    )
    return food_source


def is_fit_better(old_food_source, food_source, function):
    '''
    Check if the fitness of a food source is better than
    that of another one
    '''
    return fitness(old_food_source, function) < fitness(food_source, function)


def best_fit(old_food_source, food_source, function):
    '''
    Return the best food source, based on fitnesses
    '''
    return (
        food_source if is_fit_better(old_food_source, food_source, function)
        else old_food_source
    )


def find_best(current_best, food_sources, function):
    '''
    Return the best food source, based on fitnesses
    '''
    best_idx = np.argmax(np.apply_along_axis(
        lambda x: fitness(x, function), axis=1, arr=food_sources
    ))
    return best_fit(food_sources[best_idx], current_best, function)


def onlooker_probabilities(food_sources, function):
    '''
    Compute the probabilities of onlooker bees of moving to
    a new food source
    '''
    probabilities = np.apply_along_axis(
        lambda x: fitness(x, function), axis=1, arr=food_sources
    )
    probabilities /= np.sum(probabilities)
    return probabilities


def probability(p):
    '''
    Return True with probability p
    '''
    assert(0 <= p <= 1)
    return p > np.random.random_sample()


def renew_food_sources(food_sources, trails, limit, lower_bounds, upper_bounds):
    '''
    Scout bees stage
    '''
    n_food_sources, n_vars = food_sources.shape
    assert(n_food_sources == trails.size)

    for i, trail in enumerate(trails):
        if trail >= limit:
            j = np.random.choice(np.arange(n_vars))
            food_sources[i][j] = (
                lower_bounds[j] + np.random.random_sample() *
                (upper_bounds[j] - lower_bounds[j])
            )
    return food_sources


def move_food_sources(food_sources, trails, function, probabilities=None):
    '''
    Compute the new food sources and trails values for
    the employed and onlooker bees
    '''
    n_food_sources, _ = food_sources.shape
    for i in range(n_food_sources):
        if (probabilities is None or
                (probabilities is not None and probability(probabilities[i]))):
            food_source = new_food_source(food_sources, i)
            if is_fit_better(food_sources[i], food_source, function):
                food_sources[i] = food_source
                trails[i] = 0
            else:
                trails[i] += 1
    return food_sources, trails


def abc_algorithm(n_food_sources, lower_bounds, upper_bounds, limit, max_iterations, function):
    '''
    Main ABC algorithm
    '''
    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)
    assert(lower_bounds.size == upper_bounds.size)
    assert(lower_bounds.size > 0)
    assert(n_food_sources > 0)
    assert(limit > 0)
    assert(max_iterations > 0)

    # Initialization
    food_sources = gen_pop(n_food_sources, lower_bounds, upper_bounds)
    trails = np.zeros(n_food_sources)
    best_food_source = find_best(food_sources[0], food_sources, function)

    # Main iterations
    for _ in range(max_iterations):

        # Employed bees stage
        food_sources, trails = move_food_sources(
            food_sources, trails, function
        )
        best_food_source = find_best(best_food_source, food_sources, function)

        # Onlooker bees stage
        probabilities = onlooker_probabilities(food_sources, function)
        food_sources, trails = move_food_sources(
            food_sources, trails, function, probabilities
        )
        best_food_source = find_best(best_food_source, food_sources, function)

        # Scout bees stage
        food_sources = renew_food_sources(
            food_sources, trails, limit, lower_bounds, upper_bounds
        )

    return best_food_source


def parse_args():
    '''
    Parse standard input arguments
    '''
    parser = argparse.ArgumentParser(description='Artificial Bee Colony algorithm')
    parser.add_argument(
        dest='n_food_sources', action='store', default=10,
        type=int, help='number of food sources'
    )
    parser.add_argument(
        dest='lower_bounds', action=ListAction,
        help='lower bounds for each variable',
    )
    parser.add_argument(
        dest='upper_bounds', action=ListAction,
        help='upper bounds for each variable',
    )
    parser.add_argument(
        '-l', '--limit', action='store', default=50,
        type=int, help='trails limit'
    )
    parser.add_argument(
        '-i', '--max_iterations', action='store', default=1000,
        type=int, help='maximum number of iterations'
    )
    parser.add_argument(
        '-f', '--function', action='store', default='rosenbrock',
        type=str, choices=FUNCTIONS.keys(), help='benchmark function'
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    minimum = abc_algorithm(
        args.n_food_sources, args.lower_bounds, args.upper_bounds,
        args.limit, args.max_iterations, FUNCTIONS[args.function]
    )
    print(minimum)


if __name__ == '__main__':
    main()
