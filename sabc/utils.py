'''
Utility functions
'''


import argparse

import numpy as np


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        values = [float(x)
                  for x in values.replace('[', '').replace(']', '').split(',')]
        setattr(namespace, self.dest, values)


def print_statistics(results, mins, iterations, max_iterations, function):
    best_solution = np.argmin(mins)
    worst_solution = np.argmax(mins)
    print('Best solution:')
    print(f'\tResult: {results[best_solution]}')
    print(f'\tMinimum: {mins[best_solution]}')
    print(f'\tIterations: {iterations[best_solution]}/{max_iterations}')

    print('Worst solution:')
    print(f'\tResult: {results[worst_solution]}')
    print(f'\tMinimum: {mins[worst_solution]}')
    print(f'\tIterations: {iterations[worst_solution]}/{max_iterations}')

    mean_solution = np.mean(results, axis=0)
    print('Statistics:')
    print(f'\tMean result: {mean_solution}')
    print(f'\tMean min: {np.mean(mins)}')
    print(f'\tMean Iterations: {np.mean(iterations)}/{max_iterations}')

    print(f'\tFunction in mean result: {function(mean_solution)}')
    print(f'\tStandard deviation of mins: {np.std(mins)}')


def rosenbrock(x):
    '''
    Compute the generalized Rosenbrock function.
    In 2D, minimum 0 at (1, 1)
    '''
    y = 0
    for i in range(len(x) - 1):
        y += (100 * ((x[i + 1] - x[i] ** 2) ** 2) + (1 - x[i]) ** 2)
    return y


def sixhump(x):
    '''
    Compute the 2D six-hump camelback function.
    Minimum -1.0316 at (0.0898, -0.7126) and (-0.0898, 0.7126)
    '''
    return (
        (4 - 2.1 * (x[0] ** 2) + (x[0] ** 4) / 3.) *
        (x[0] ** 2) + x[0] * x[1] + (-4 + 4 * (x[1]**2)) * (x[1] ** 2)
    )


def rastrigin(x):
    '''
    Compute the Rastrigin function.
    Minimum 0 at (0, ..., 0)
    '''
    return (10 * x.size) + np.sum((x ** 2) - 10 * np.cos(2 * np.pi * x))


def ackley(x):
    '''
    Compute the Ackley function.
    Minimum 0 at (0, ..., 0)
    '''
    return (
        (20 - 20 * np.exp(-0.2 * np.sqrt((1/x.size) * np.sum(x**2)))
         + np.exp(1) - np.exp((1 / x.size) * np.sum(np.cos(2 * np.pi * x))))
    )


FUNCTIONS = {
    'rosenbrock': rosenbrock,
    'sixhump': sixhump,
    'rastrigin': rastrigin,
    'ackley': ackley
}
