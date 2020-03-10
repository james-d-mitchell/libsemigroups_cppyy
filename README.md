# libsemigroups_cppyy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/libsemigroups/libsemigroups_cppyy/master?filepath=demo.ipynb)
[![Build Status](https://travis-ci.org/libsemigroups/libsemigroups_cppyy.svg?branch=master)](https://travis-ci.org/libsemigroups/libsemigroups_cppyy)

libsemigroups_cppyy is an experimental package for using the C++ library
[libsemigroups](https://libsemigroups.readthedocs.io/en/latest/)
in python via [cppyy](https://cppyy.readthedocs.io/en/latest/).

## Installation

Install
[libsemigroups](https://github.com/libsemigroups/libsemigroups), via its sources or conda package.

By conda:
Add conda-forge to an installation of anaconda:

    conda config --add channels conda-forge
    
And then download libsemigroups, specifying the version (1.0.6)

    conda install libsemigroups=1.0.6

Then install cppyy and networkx via conda or pip:
    
    conda install cppyy
    conda install networkx

To use cppyy, note you will need gcc. 

Finally, for normal use, git clone this repository and then run:

    pip install .

Refer to demo.ipynb for more functionality. 

## Docker

If you have [Docker](https://www.docker.com) installed, you can download this container using:
~~~
docker pull libsemigroups/libsemigroups_cppyy
~~~

The docker container for `libsemigroups_cppyy` can be started by typing:
~~~
docker run --rm -it libsemigroups/libsemigroups_cppyy
~~~
and in the docker container you can start python by typing:
~~~
python3
~~~

Load the `libsemigroups_cppyy` package in python by typing
~~~
import libsemigroups_cppyy
~~~
