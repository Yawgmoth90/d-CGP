[![DOI](https://zenodo.org/badge/38923383.svg)](https://zenodo.org/badge/latestdoi/38923383)
[![Build status](https://ci.appveyor.com/api/projects/status/0krbaimpvjx76fcm?svg=true)](https://ci.appveyor.com/project/darioizzo/d-cgp)
[![Build Status](https://travis-ci.org/darioizzo/d-CGP.svg?branch=master)](https://travis-ci.org/darioizzo/d-CGP)
[![PyPI](https://img.shields.io/badge/pypi-v1.0.1-blue.svg)](https://pypi.python.org/pypi?:action=display&name=dcgpy&version=1.0.1)

# d-CGP
Implementation of differentiable Cartesian Genetic Programming (d-CGP)

The d-CGP is a recent development in the field of Genetic Programming that adds the information about the derivatives of the output nodes (the programs, or expressions encoded) with respect to the input nodes (the input values) and weights. In doing so, it enables a number of new applications currently the subject of active research.

 * The evolution of the genetic program can now be helped by using the information on the derivatives, enabling for the equivalent of backpropagation in Neural Networks.
 * The fitness function can be defined in terms of the derivatives, allowing to go beyond simple regression tasks and, instead, solve differential equations, learn differential models, capture conserved quantities in dynamical systems.
 
The first research paper describing d-CGP use to solve symbolic regressions problems such is:

Izzo, Dario, Francesco Biscani, and Alessio Mereta. "Differentiable Genetic Programming." arXiv preprint arXiv:1611.04766 (2016).

## dcgpy
If you have a win 64bit system or a linux based system (32 or 64 bits), the python package dcgpy (python binding of the C++ code) can be installed via:

 ```pip install dcgpy```

otherwise you will have to compile it by activating the BUILD_DCGPY option in CMake

## Compiling the source code or using the header only library
### Dependencies
Several and tested dependencies are necessary to succesfully compile d-CGP
 * Audi, headers only library - (git clone https://github.com/darioizzo/audi.git)
 * Piranha, headers only library - (git clone https://github.com/bluescarni/piranha.git)
 * Boost, headers only
 
If you have all this, after cloning the git repository, go into mit and type ```git submodule init```, ```git submodule update``` and you are good to go! (these last commands clone the pybind11 code necessary to create the python bindings)

## Other CGP libraries
### Comparison to the CGP-Library
If all below statements are true:
 * You do not care about knowing derivatives of your encoded program
 * You do not care about run-time capabilities
 * You do not care about the Python module
 * You do not care about the possibility of defining your kernel functions as complex functors (e.g. CGP expressions.)
 * You do not care about thread-safety

then you should consider using, instead, Andrew Turner's CGP-Library (http://www.cgplibrary.co.uk/files2/About-txt.html) which is, roughly, twice as fast to compute a CGP expression as it makes use of function pointers rather than a std::function to define the kernel functions.
