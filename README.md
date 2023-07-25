# GScrew (Generalized Screw Calculus)
[![Documentation Status](https://readthedocs.org/projects/gscrew/badge/?version=latest)](https://gscrew.readthedocs.io/en/latest/?badge=latest)
[![Licence](https://img.shields.io/github/license/Shadow15510/GScrew?color=green)](https://github.com/Shadow15510/GScrew/blob/master/LICENSE)

## Description
A Python module to manipulate Screws and Coscrews with geometrics algebra (Clifford's Algebra).

The full documentation is on readthedocs.

If you encounter an issue, feel free to open one.

## Installation
A Pypi package is available, please refer to the Pypi page or enter `pip install gscrew` in a terminal.

## Exemples
First of all, you need to import the modules:
```
import geometric_algebra as ga
from screw import Screw
```
The `screw` module also provides a `CoScrew` object and the `comoment` function for calculating the comoment between a coscrew and a screw.

Once these modules have been imported, we can create the geometric algebra in which we will be working. For basic physical applications, a three-dimensionnal algebra should suffice:
```
my_algebra = ga.GeometricAlgebra(3)
locals().update(my_algebra.blades)
```
The second line adds the basis blades to the local variables so that we will be able to create new multivectors just by performing linear combinations of these basis blades. For a 3D algebra, the basis blades are: e0, e1, e2, e3, e12, e13, e32, e123.

We can now start working with Screw and CoScrew classes:
```
O = 0 * e0  # the origin of the reference frame
S = 1 + (2*e2) + (3*e3)  # the direction of the screw
M = (e1) + (5*e3)        # the moment of the screw
my_screw = Screw(O, S, M)
```

## Licence
All the code is provided under the GNU General Public Licence v3.0+ (GPLv3+)
