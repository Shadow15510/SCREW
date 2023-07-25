Basic use
=================

Installing the package
----------------------
GScrew is deployed on Pypi, so the easiest way to install the package is to run the following command: ``pip install gscrew``. To force pip to use a Python3 environement, you can replace ``pip`` with ``pip3``.

If pip is not install on your machine, you can clone the repository by running: ``git clone https://github.com/Shadow15510/GScrew.git``.

.. note:: For this second option, you need to have git installed.

Importing the package
---------------------
Once GScrew is installed, you should import it as following::
	
	import gscrew.geometric_algebra as ga
	from gscrew.screw import Screw, CoScrew, comoment

The ``geometric_algebra`` module is a framework which provides you with a n-dimensional geometric algebra and multivectors.

The ``screw`` module gives you three main objects:

* Screw, a class which implements generalized screws

* CoScrew, also a class, implementing coscrews

* comoment, a function implementing the comoment of a coscrew and a screw

Initializing the framework
--------------------------
Before manipulating screws, you need to initialize the geometric algebra in which you will work. For the exemple, we work with a three-dimensionnal one but the module can handle n-dimensional algebras::

	my_algebra = ga.GeometricAlgebra(3)
	locals().update(my_algebra.blades)

On the first line, we create a new three-dimensional algebra. On the second one we add the basis blades to the local variables. It will allow you to use the basis blades (such as ``e0``, ``e1``, ``e2``… ``e12``… ``e123`` etc) to create new multivectors.

Finally creating a screw
------------------------
Once the geometric algebra has been initialized, you can start working with screws. Each screw (this also applies to coscrews) is composed of three elements:

* the reference point at which the screw is expressed

* the direction of the screw (which is independent of the reference point)

* the moment of the screw (which depends on the reference point)

.. note:: The ``Screw`` and ``CoScrew`` classes inherit from a more general class: ``ScrewBase``. So when a manipulation or a method is introduced as a ``ScrewBase`` method, it will operate on ``Screw`` and ``CoScrew`` classes.

So let's see a small exemple::

	A = e1 + e2  # the point A(1, 1, 0)
	S1 = 1*e0    # e0 is the scalar dimension
	M1 = 2*e2    # this is a simple vector
	screw1 = Screw(A, S, M)

To display a screw, you can print it, but it is recommended to use the method ``ScrewBase.show``. Indeed, the moment of a screw depends on the chosen point of reduction, so by using ``ScrewBase.show`` you can pass the point at which you want to display the screw::

	screw1.show()  # will display the screw on the reference point, here A
	screw1.show(0 * e0)  # will display the screw on the origin of the reference frame

.. note::
	``print`` will display the screw at its reference point.

You can also change the reference point of a screw by using ``ScrewBase.change_point``::
	
	B = e1 - e2  # let be B a new point
	screw2 = screw1.change_point(B)
	print(screw1 ^ screw2)  # returns the zero screw

In this case, for example, ``screw1`` and ``screw2`` are the same 1-screw but are not expressed at the same point. So the straight line joining these two 1-screws does not exist, hence the zero screw.
