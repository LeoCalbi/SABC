# SABC

This repository contains the implementation of the following optimization methods:

- **Artificial Bee Colony** [[1]](#1)
- **Nelder-Mead** [[2]](#2)
- **Simplex Artificial Bee Colony** [[3]](#3)

The implemented methods are supposed to work for unconstrained non-linear minimization problems.\
You can check the convergence properties of each of the algorithms in their corresponding reference paper.

## Installation

This project was written and tested with `Python 3.7`, so make sure that you have it installed on your system.\
The libraries required by the project are listed in the `requirements.txt` file. You can install them by running:

```bash
pip install -r requirements.txt
```

The core of the project is inside the `sabc` Python package, which has the following modules:

- `abeec.py`, which contains the implementation of the **ABC** algorithm
- `amoeba.py`, which contains the implementation of the **Nelder-Mead** algorithm
- `sabeec.py`, which contains the implementation of the **SABC** algorithm

## Usage

You can run each of the three algorithms separately. To check the required fields, `cd` into the `sabc` folder and run:

```bash
python3 <alg>.py -h
```

Here, `<alg>` could be one of `abeec`, `amoeba` or `sabeec`.

### ABC Parameters

- `n_food_sources`: Number of food source to find inside the given bounds, represents also the number of employed, onlooker bees. (default 100)
- `lower_bounds`: List of numbers representing the lower bounds of each variable in the search space, must have the same size as `upper_bounds` (they define the dimension of the search space).
- `upper_bounds`: List of numbers representing the upper bounds of each variable in the search space.
- `limit`: Upper limit of trail before abandoning a food source. (default 20)
- `abc_iterations`: Maximum number of iterations for the ABC algorithm. (default 3000)
- `abc_stop`: Maximum number of non-changing best value before stopping the algorithm. (default 100)
- `function`: Function on with to execute the search. (default 'rosenbrock')
- `runtimes`: Number of executions for statistics purposes. (default 1)

### Nelder-Mead Parameters

- `initial_point`: Initial point used to compute the simplex.
- `nm_iterations`: Maximum number of iterations for the Nelder-Mead algorithm. (default 3000)
- `tol`: Tolerance for the stopping criteria of the algorithm. (default $10^{-5}$)
- `alpha`: Coefficient for the reflection operation. (default 1)
- `beta`: Coefficient for the contraction operation. (default 0.5)
- `gamma`: Coefficient for the expansion operation. (default 2)
- `function`: Function on with to execute the search. (default 'rosenbrock')

### SABC Parameters

As a combination of the two algorithms takes all the above parameters, except `initial_point` of Nelder-Mead because it's computed by the ABC procedure.

## Implemented Functions

The benchmark functions you can choose are implemented in the `utils.py` module:

- `ackley` $f(x_1 \cdots x_n) = -20 exp(-0.2 \sqrt{\frac{1}{n} \sum_{i=1}^n x_i^2}) - exp(\frac{1}{n} \sum_{i=1}^n cos(2\pi x_i)) + 20 + e$
- `rastrigin` $f(x_1 \cdots x_n) = 10n + \sum_{i=1}^n (x_i^2 -10cos(2\pi x_i))$
- `rosenbrock` $f(x_1 \cdots x_n) = \sum_{i=1}^{n-1} (100(x_i^2 - x_{i+1})^2 + (1-x_i)^2)$
- `sixhump` $f(x_1,x_2)=(4 - 2.1x^2_1+\frac{1}{3}x^4_1) * (x_1^2 +x_1x_2 -4+4x^2_2) * (x_2^2)$

## Use cases

Below you can find some examples to run the different modules:

### ABC

```bash
python abeec.py 100 '[-10, -10]' '[10, 10]' -l 20 -i 1000 -c 50 -f 'rosenbrock'
```

### Nelder-Mead

```bash
python amoeba.py '[10, 10]' -i 1000 -f 'rosenbrock'
```

### SABC

```bash
python sabeec.py 100 '[-10, -10]' '[10, 10]' -c 50 -l 20 --nm_iterations 100 --abc_iterations 1000 -f 'rosenbrock'
```

## References

- <a id="1">[1]</a>
  _Dervis Karaboga and Bahriye Basturk (2007)_.\
  **Artificial Bee Colony (ABC) Optimization Algorithm for Solving Constrained Optimization Problems**.\
  Erciyes University, Engineering Faculty, The Department of Computer Engineering
- <a id="2">[2]</a>
  _J. A. Nelder and R. Mead (1965)_.\
  **A simplex method for function minimization**.\
  The Computer Journal, 7(4), 308-313.
- <a id="3">[3]</a>
  _Xufang Zhao, Ximing Liang, Long Wen (2018)_.\
  **The Artificial Bee Colony Algorithm Improved with Simplex Method**.\
  School of Science, Beijing University of Civil Engineering and Architecture.
- <a id="4">[4]</a>
  _Fuchang Gao, Lixing Han (2010)_.\
  **Implementing the Nelder-Mead simplex algorithm with adaptive parameters**.\
  Springer Science+Business Media, LLC 2010.
