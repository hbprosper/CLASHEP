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
If all goes well, this will install a recent version of the [ROOT](https://root.cern.ch) package from CERN as well as *Python* and several Python modules including *numpy*.

#### Step 3
Install *pytorch*, *matplotlib*, *scikit-learn*, etc.
```bash
	conda install –c conda-forge pytorch
	conda install –c conda-forge matplotlib
	conda install –c conda-forge scikit-learn
	conda install –c conda-forge pandas
	conda install –c conda-forge sympy
	conda install –c conda-forge imageio
	conda install –c conda-forge jupyter
```

#### Step 4
Install __git__ if it is not yet on your system, then download the CLASHEP package.
```bash
	conda install –c conda-forge git
	mkdir tutorials
	cd tutorials
	git clone https://github.com/hbprosper/CLASHEP
```
In the above the package CLASHEP has been downloaded into a directory called *tutorials*.

#### Step 5

Open a new terminal window, navigate to the parent directory that contains CLASHEP, and run the jupyter notebook in that window (in blocking mode).
```bash
	jupyter notebook
```
If all goes well, the jupyter notebook will appear in your default browser. 
Navigate to the CLASHEP directory and under the *Files* menu item, click on the notebook *test.ipynb* and execute it. This notebook tries to import several Python modules. If it does so without error messages, you are ready to try out the other notebooks.


## Examples

### Statistics
| __notebook__   | __description__     |
| :---          | :---        |
| 03_rootn         | coverage of root(N) upper limits     |
| 03_wilks    | Wilks' theorem |
| 05_profile_likelihood     | calculation of profile likelihood for a signal/background problem |


### Machine Learning
| __notebook__   | __description__     |
| :---          | :---        |
| hzz4l_sklearn         | Boosted Decision Trees (BDT) with AdaBoost: classification of Higgs boson events    |
| hzz4l_pytorch    | Deep Neural Network (DNN): classification of Higgs boson events |
| autoencoder1d    | Autoencoder: map SDSS galaxy/quasar data to 1D |
| mnist_cnn        | Convolutional Neural Network (CNN): classification of MNIST digits |
| 01_phantom..., 02_phantom..., 03_phantom... | Simulation-Based Inference (SBI): infer parameters of a 2-parameter cosmological model using simulation-based inference. The first notebook generates the simulated Type 1a data; the 2nd notebook performs the simulaiton-based inference, while the 3rd notebook checks the coverage of the confidence sets. The 2-parameter cosmological model is described in phantom_model.ipynb|
