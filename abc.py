import numpy as np
import argparse
from scipy.optimize import rosen


def gen_pop(n_food_sources, lower_bounds, upper_bounds):
    n_vars = len(lower_bounds)
    if n_vars != len(upper_bounds):
        raise Exception()
    food_sources = []
    for _ in range(n_food_sources):
        food_source = list(lower_bounds)
        for i in range(n_vars):
            food_source[i] += np.random.random_sample() * \
                (upper_bounds[i]-lower_bounds[i])
        food_sources.append(food_source)
    return food_sources


def fitness(food_source, function):
    value = function(food_source)
    return 1/(1+value) if value >= 0 else 1+abs(value)


def new_food_source(food_sources, index):
    n_food_sources = len(food_sources)
    n_vars = len(food_sources[index])
    d = np.random.choice(range(n_vars))
    other_indexes = list(range(n_food_sources))
    other_indexes.remove(index)
    new_index = np.random.choice(other_indexes)
    food_source = list(food_sources[index])
    food_source[d] += np.random.uniform(-1, 1) * \
        (food_source[d]-food_sources[new_index][d])
    return food_source


def is_fit_better(old_food_source, food_source, function):
    return fitness(old_food_source, function) < fitness(food_source, function)


def onlooker_probabilities(food_sources, function):
    probabilities = np.array([fitness(f, function) for f in food_sources])
    probabilities /= np.sum(probabilities)
    return probabilities


def probability(p):
    '''
    Return True with probability p
    '''
    return p > np.random.random_sample()


def renew_food_sources(food_sources, trails, limit, lower_bounds, upper_bounds):
    for index, trail in enumerate(trails):
        if trail >= limit:
            j = np.random.choice(range(len(food_sources[index])))
            food_sources[index][j] = lower_bounds[j] + \
                np.random.random_sample()*(upper_bounds[j]-lower_bounds[j])
    return food_sources


def find_best(best_food_source, food_sources, function):
    for food_source in food_sources:
        if is_fit_better(best_food_source, food_source, function):
            best_food_source = food_source
    return best_food_source


def rosenbrock_function(x):
    y = 0
    for i in range(len(x)-1):
        y += (100*((x[i+1]-x[i]**2)**2)+(1-x[i])**2)
    return y


def sixhump(x):
    return ((4 - 2.1*x[0]**2 + x[0]**4 / 3.) * x[0]**2 + x[0] * x[1]
            + (-4 + 4*x[1]**2) * x[1] ** 2)


def abc_algorithm(n_food_sources, lower_bounds, upper_bounds, limit, max_iterations, function):

    food_sources = gen_pop(n_food_sources, lower_bounds, upper_bounds)
    trails = [0] * len(food_sources)
    best_food_source = food_sources[0]

    best_food_source = find_best(best_food_source, food_sources, function)

    for _ in range(max_iterations):

        for index in range(n_food_sources):
            food_source = new_food_source(food_sources, index)
            if is_fit_better(food_sources[index], food_source, function):
                food_sources[index] = food_source
                trails[index] = 0
            else:
                trails[index] += 1

        best_food_source = find_best(best_food_source, food_sources, function)

        probabilities = onlooker_probabilities(food_sources, function)

        for index in range(n_food_sources):
            if probability(probabilities[index]):
                food_source = new_food_source(food_sources, index)
                if is_fit_better(food_sources[index], food_source, function):
                    food_sources[index] = food_source
                    trails[index] = 0
                else:
                    trails[index] += 1

        best_food_source = find_best(best_food_source, food_sources, function)

        food_sources = renew_food_sources(
            food_sources, trails, limit, lower_bounds, upper_bounds)

    return best_food_source


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = [float(x)
                  for x in values.replace('[', '').replace(']', '').split(',')]
        setattr(namespace, self.dest, values)


def parse_args():
    '''
    Parse standard input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Artificial bee colony algorithm')
    parser.add_argument(
        dest='n_food_sources',
        action='store',
        default=10,
        type=int,
        help='number of food sources'
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
        dest='limit',
        action='store',
        default=50,
        type=int,
        help='trails limit'
    )
    parser.add_argument(
        dest='max_iterations',
        action='store',
        default=1000,
        type=int,
        help='maximum number of iterations'
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(args)
    minimum = abc_algorithm(args.n_food_sources, args.lower_bounds,
                            args.upper_bounds, args.limit, args.max_iterations, sixhump)
    print(minimum)
    print(sixhump([-0.0898, 0.7126]))
    print(sixhump(minimum))


if __name__ == '__main__':
    main()
