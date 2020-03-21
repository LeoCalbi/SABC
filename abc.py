import numpy as np


def gen_pop(n_food_sources, lower_bounds, upper_bounds):
    n_vars = len(lower_bounds)
    if n_vars != len(upper_bounds):
        raise Exception()
    food_sources = []
    for _ in range(n_food_sources):
        food_source = []
        for i in range(n_vars):
            food_source[i] = lower_bounds[i] + \
                np.random.random_sample()*(upper_bounds[i]-lower_bounds[i])
        food_sources.append(food_source)
    return food_sources


def fitness(food_source, function):
    value = function(food_source)
    return 1/(1+value) if value >= 0 else 1+abs(value)


def new_food_source(food_sources, index):
    n_food_sources = len(food_sources)
    n_vars = len(food_sources[0])
    d = np.random.choice(range(n_vars))
    new_index = np.random.choice(range(n_vars).remove(index))
    food_source = food_sources[index]
    food_source[d] += np.random.uniform(-1, 1) * \
        (food_source[d]-food_sources[new_index][d])
    return food_source


def is_fit_better(old_food_source, new_food_source, function):
    return fitness(old_food_source, function) < fitness(new_food_source, function)


def onlooker_probabilities(food_sources, function):
    probabilities = [fitness(f, function) for f in food_sources]
    probabilities /= sum(probabilities)
    return probabilities


def probability(p):
    '''
    Return True with probability p
    '''
    return p > np.random.random_sample()


