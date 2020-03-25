'''
Nelder-Mead algorithm
'''


import argparse

import numpy as np

from utils import *


def downhill_simplex(simplex, function, max_iterations, tol, alpha, beta, gamma):
    assert(alpha > 0)
    assert(0 < beta < 1)
    assert(gamma > 1)
    assert(tol > 0)
    assert(max_iterations > 0)

    v = np.apply_along_axis(function, axis=1, arr=simplex)
    iterations = 0
    h = -1
    l = 0
    for it in range(max_iterations):
        iterations = it
        if stop_criteria(v, tol):
            break

        # Sort values and simplex
        sorted_indexes = np.argsort(v)
        v = v[sorted_indexes]
        simplex = simplex[sorted_indexes]

        centroid = np.mean(simplex[:h], axis=0)
        x_prime = reflection(alpha, centroid, simplex[h])
        y_prime = function(x_prime)
        is_y_prime_best = (
            (y_prime > v[:h]).sum() == v[:h].size
        ).astype(np.int)

        if y_prime < v[l]:
            x_second = expansion(gamma, centroid, x_prime)
            y_second = function(x_second)
            if y_second < v[l]:
                simplex[h] = x_second
                v[h] = y_second
            else:
                simplex[h] = x_prime
                v[h] = y_prime
        elif is_y_prime_best:
            if y_prime <= v[h]:
                simplex[h] = x_prime
                v[h] = y_prime
            x_second = contraction(beta, centroid, simplex[h])
            y_second = function(x_second)
            if y_second > v[h]:
                simplex = shrink(simplex, l)
                v = np.apply_along_axis(function, axis=1, arr=simplex)
            else:
                simplex[h] = x_second
                v[h] = y_second
        else:
            simplex[h] = x_prime
            v[h] = y_prime

    return simplex[np.argmin(v)], iterations


def reflection(alpha, centroid, point):
    return (1 + alpha) * centroid - alpha * point


def expansion(gamma, centroid, point):
    return (1 + gamma) * point - gamma * centroid


def contraction(beta, centroid, point):
    return beta * point + (1 - beta) * centroid


def shrink(simplex, l):
    x_min = simplex[l]
    return np.apply_along_axis(
        lambda x: (x + x_min) / 2, axis=1, arr=simplex
    )


def stop_criteria(v, tol):
    mu = np.mean(v)
    n = len(v)
    return np.sqrt(
        np.sum(
            np.apply_along_axis(lambda x: x ** 2, axis=0, arr=(v - mu))
        ) / n
    ) <= tol


def simplex_coordinates(x_zero):
    '''
    Generate a simplex starting from the given initial point.
    Implementation based upon Matlab's fminsearch routine.
    '''
    x = [np.array(x_zero)]
    n = len(x_zero)
    b = np.eye(n)
    for i in range(n):
        h = (
            0.05 if x_zero[i] != 0
            else 0.00025
        )
        x.append(x_zero + h * b[i])
    return np.array(x)


def parse_args():
    '''
    Parse standard input arguments
    '''
    parser = argparse.ArgumentParser(
        description='Nelder-Mead downhill simplex algorithm'
    )
    parser.add_argument(
        dest='initial_point', action=ListAction,
        help='initial point used to compute the simplex'
    ),
    parser.add_argument(
        '-i', '--max_iterations', action='store', default=1000,
        type=int, help='maximum number of iterations'
    ),
    parser.add_argument(
        '-t', '--tol', action='store', default=1e-5,
        type=float, help='tolerance for the stopping criteria'
    ),
    parser.add_argument(
        '-a', '--alpha', action='store', default=1,
        type=float, help='coefficient for reflection'
    ),
    parser.add_argument(
        '-b', '--beta', action='store', default=0.5,
        type=float, help='coefficient for contraction'
    ),
    parser.add_argument(
        '-g', '--gamma', action='store', default=2,
        type=float, help='coefficient for expansion'
    )
    parser.add_argument(
        '-f', '--function', action='store', default='rosenbrock',
        type=str, choices=FUNCTIONS.keys(), help='benchmark function'
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    simplex = simplex_coordinates(args.initial_point)
    print(f'Initial simplex: {simplex}')
    result, iterations = downhill_simplex(
        simplex, FUNCTIONS[args.function], args.max_iterations,
        args.tol, args.alpha, args.beta, args.gamma
    )
    print(f'Result: {result}')
    print(f'Iterations: {iterations}')


if __name__ == "__main__":
    main()
