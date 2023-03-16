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
Assuming conda is properly installed and initialized on your laptop, you can create an environment, here we call it *clashep*, containing the __root__ package from CERN, plus a large subset of the packages in the conda system, using the command>
```bash
conda create -c conda-forge --name clashep root
```
Before pressing __y__ to continue with the installation, scan through the list of packages and identify which of the above are in the list. That way, you will know which ones are missing and need to be installed using the conda install command. For example, as of this writing __pytorch__ is not available by default. In order to install a missing packages, first be sure to choose the conda environment into which the package is to be installed. First activate the desired environment, by doing, for example,
```bash
conda activate clashep
```
Later, in order to update root together with a consistent set of packages do
```bash
conda update root
```
taking care to do so in the desired conda environment, here __clashep__.
