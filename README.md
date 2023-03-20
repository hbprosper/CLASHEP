# CERN Latin-American School of High-Energy Physics (CLASHEP)
## Introduction
This repository contains jupyter notebooks on statistics and machine learning associated with the lectures at this school.


## Dependencies
The notebooks in this package depend on several well-known Python
modules, all well-engineered and free!

| __modules__   | __description__     |
| :---          | :---        |
| pandas        | data table manipulation, often with data loaded from csv files |
| numpy         | array manipulation and numerical analysis      |
| matplotlib    | a widely used plotting module for producing high quality plots |
| imageio      | photo-quality image display module |
| scikit-learn  | easy to use machine learning toolkit |
| pytorch       | a powerful, flexible, machine learning toolkit |
| scipy         | scientific computing    |
| sympy        | an excellent symbolic mathematics module |
| iminuit | an elegant wrapper around the venerable CERN minimizer Minuit |
| emcee | an MCMC module |
| tqdm         | progress bar |
| joblib | module to save and load Python object |
| importlib | importing and re-importing modules |


##  Installation
The simplest way to install these Python modules is first to install miniconda (a slim version of Anaconda) on your laptop by following the instructions at:

https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

I recommend installing miniconda3, which comes pre-packaged with Python 3.

Software release systems such as Anaconda (__conda__ for short) make
it possible to have several separate self-consistent named
*environments* on a single machine, say your laptop. For example, you
may need to use Python 3.7.5 and an associated set of compatible
packages and at other times you may need to use Python 3.9.13 with
packages that require that particular version of Python.  If you install software without using *environments* there is
the danger that the software on your laptop will eventually become
inconsistent. Anaconda (and its lightweight companion miniconda)
provide a way, for example, to create a software *environment*
consistent with Python 3.7.5 and another that is consistent with
Python 3.9.13.  For example,
one package may work only with a given version of numpy, while another
requires a different version. In principle, having different versions of numpy on
your machine, just
like having different versions of Python, is not a problem if one uses
environments.

Of course, like anything human beings make, miniconda3 is not
perfect. There are times when the only solution is to delete an
environment and rebuild by reinstalling the desired packages.

### Miniconda3

After installing miniconda3, It is a good idea to update conda using the command
```bash
conda update conda
```
#### Step 1 
Assuming conda is properly installed and initialized on your laptop, you can create an environment, here called *clashep*. 
```bash
conda create --name clashep
```
and activate it by doing
```bash
conda activate clashep
```
You need create the environment only once, but you nust activate and environment whenever you create a new terminal window.

#### Step 2 
Install root, python, numpy, …
```
	conda install –c conda-forge root
```
If all goes well, this will install a recent version of the [https://root.cern.ch](ROOT) from CERN.
