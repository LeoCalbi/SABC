# SABC

This repository contains the implementation of the following methods:
- **Artificial Bee Colony**
- **Nelder-Mead**
- **Simplex Artificial Bee Colony**

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
For example, if you choose `<alg>` to be `abeec`, the output will be like:
```
usage: abeec [-h] [-l LIMIT] [-i ABC_ITERATIONS] [-c ABC_STOP]
             [-f {rosenbrock,sixhump}]
             n_food_sources lower_bounds upper_bounds

Artificial Bee Colony algorithm

positional arguments:
  n_food_sources        number of food sources
  lower_bounds          lower bounds for each variable
  upper_bounds          upper bounds for each variable

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        trails limit
  -i ABC_ITERATIONS, --abc_iterations ABC_ITERATIONS
                        maximum number of iterations
  -c ABC_STOP, --abc_stop ABC_STOP
                        maximum number of non-changing best value before
                        stopping
  -f {rosenbrock,sixhump}, --function {rosenbrock,sixhump}
                        benchmark function
```

The benchmark functions you can choose are implemented in the `utils.py` module.

## Use cases

Below you can find some examples to run the different modules:

_ABC_
```bash
python abeec.py 100 '[-10, -10]' '[10, 10]' -l 20 -i 1000 -c 50 -f 'rosenbrock'
```

_Nelder-Mead_
```bash
python amoeba.py '[10, 10]' -i 1000 -f 'rosenbrock'
```

_SABC_
```bash
python sabeec.py 100 '[-10, -10]' '[10, 10]' -c 50 -l 20 --nm-iterations 100 --abc-iterations 1000 -f 'rosenbrock'
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
_Fuchang Gao, Lixing Han_.\
**Implementing the Nelder-Mead simplex algorithm with adaptive parameters**.\
Springer Science+Business Media, LLC 2010
