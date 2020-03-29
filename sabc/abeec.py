'''
Artificial Bee Colony algorithm
'''


import argparse
import time

import numpy as np

from utils import ListAction, FUNCTIONS, print_statistics


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


def new_food_source(food_sources, lower_bounds, upper_bounds, index):
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

    # Shift onto boundaries
    if food_source[d] > upper_bounds[d]:
        food_source[d] = upper_bounds[d]
    elif food_source[d] < lower_bounds[d]:
        food_source[d] = lower_bounds[d]

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


def find_current_best(current_best, food_sources, function):
    '''
    Return the best food source or the current best, based on fitnesses
    '''
    return best_fit(find_best(food_sources, function), current_best, function)


def find_best(food_sources, function):
    '''
    Return the best food source, based on fitnesses
    '''
    best_idx = np.argmax(np.apply_along_axis(
        lambda x: fitness(x, function), axis=1, arr=food_sources
    ))
    return food_sources[best_idx]


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


def renew_food_sources(food_sources, trails, limit, lower_bounds, upper_bounds, function, *args):
    '''
    Scout bees stage
    '''
    n_food_sources, n_vars = food_sources.shape
    assert(n_food_sources == trails.size)

    for i, trail in enumerate(trails):
        if trail >= limit:
            food_sources[i] = renew_food_source(food_sources[i], lower_bounds, upper_bounds)
            trails[i] = 0
    return food_sources


def renew_food_source(food_source, lower_bounds, upper_bounds):
    '''
    Compute a new food source for the scout bees stage
    '''
    n_vars = food_source.size
    j = np.random.choice(np.arange(n_vars))
    food_source[j] = (
        lower_bounds[j] + np.random.random_sample() *
        (upper_bounds[j] - lower_bounds[j])
    )
    return food_source


def move_food_sources(food_sources, lower_bounds, upper_bounds,
                      trails, function, probabilities=None):
    '''
    Compute the new food sources and trails values for
    the employed and onlooker bees
    '''
    n_food_sources, _ = food_sources.shape
    for i in range(n_food_sources):
        if (probabilities is None or
                (probabilities is not None and probability(probabilities[i]))):
            food_source = new_food_source(food_sources, lower_bounds, upper_bounds, i)
            if is_fit_better(food_sources[i], food_source, function):
                food_sources[i] = food_source
                trails[i] = 0
            else:
                trails[i] += 1
    return food_sources, trails


def abc_algorithm(n_food_sources, lower_bounds, upper_bounds, limit,
                  abc_stop, abc_iterations, function, *args):
    '''
    Main ABC algorithm
    '''
    lower_bounds = np.array(lower_bounds)
    upper_bounds = np.array(upper_bounds)
    assert(lower_bounds.size == upper_bounds.size)
    assert(lower_bounds.size > 0)
    assert(n_food_sources > 0)
    assert(limit > 0)
    assert(abc_iterations > 0)

    # Initialization
    food_sources = gen_pop(n_food_sources, lower_bounds, upper_bounds)
    trails = np.zeros(n_food_sources)
    best_food_source = find_best(food_sources, function)

    # Main iterations
    best_equal = 0
    iterations = 1
    for it in range(abc_iterations):
        iterations = it + 1

        # Employed bees stage
        food_sources, trails = move_food_sources(
            food_sources, lower_bounds, upper_bounds, trails, function
        )
        prev_best = best_food_source
        best_food_source = find_current_best(best_food_source, food_sources, function)
        best_equal = best_equal + 1 / 3 if np.array_equal(prev_best, best_food_source) else 0

        # Onlooker bees stage
        probabilities = onlooker_probabilities(food_sources, function)
        food_sources, trails = move_food_sources(
            food_sources, lower_bounds, upper_bounds, trails, function, probabilities
        )
        prev_best = best_food_source
        best_food_source = find_current_best(best_food_source, food_sources, function)
        best_equal = best_equal + 1 / 3 if np.array_equal(prev_best, best_food_source) else 0

        # Scout bees stage
        food_sources = renew_food_sources(
            food_sources, trails, limit, lower_bounds, upper_bounds, function, *args
        )
        prev_best = best_food_source
        best_food_source = find_current_best(best_food_source, food_sources, function)
        best_equal = best_equal + 1 / 3 if np.array_equal(prev_best, best_food_source) else 0

        # Stop criteria
        if best_equal >= abc_stop:
            break

    return best_food_source, iterations


def abc_cli_parser():
    '''
    Create a standard input arguments parser
    '''
    parser = argparse.ArgumentParser(prog='abeec', description='Artificial Bee Colony algorithm')
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
        '-l', '--limit', action='store', default=20,
        type=int, help='trails limit'
    )
    parser.add_argument(
        '-i', '--abc_iterations', action='store', default=1000,
        type=int, help='maximum number of iterations'
    )
    parser.add_argument(
        '-c', '--abc_stop', action='store', default=50,
        type=int, help='maximum number of non-changing best value before stopping'
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
    parser = abc_cli_parser()
    args = parser.parse_args()
    results = []
    mins = []
    iterations = []
    times = []
    for _ in range(args.runtimes):
        start_time = time.time()
        result, n_iteration = abc_algorithm(
            args.n_food_sources, args.lower_bounds, args.upper_bounds,
            args.limit, args.abc_stop, args.abc_iterations, FUNCTIONS[args.function]
        )
        times.append(time.time() - start_time)
        results.append(result)
        iterations.append(n_iteration)
        mins.append(FUNCTIONS[args.function](result))

    # Print results
    if args.runtimes == 1:
        print(f'Result: {results[0]}')
        print(f'Minimum: {mins[0]}')
        print(f'Iterations: {iterations[0]}/{args.nm_iterations}')
        print(f'Execution time: {times[0]} seconds')
    else:
        print_statistics(results, mins, iterations, args.abc_iterations, FUNCTIONS[args.function])
        print(f'Mean execution time: {np.mean(times)} seconds')
        print(f'Total execution time: {np.sum(times)} seconds')


if __name__ == '__main__':
    main()
