"""
This module provides two classes that respectively implement a screw and a co-screw.

Classes
-------
.. autoclass:: ScrewBase
.. autoclass:: Screw
.. autoclass:: CoScrew

Functions
---------
.. autofunction:: comoment

Exemples
--------
Before using theses objects, you should import the ``geometric_algebra`` module so that you can
create multivectors. For basic physical applications, a three-dimensional should be enough, but you
can use n-dimensional multivectors.

Let's see a minimal exemple::

    >>> import geometric_algebra as ga
    >>> from screw import Screw
    >>> my_algebra = ga.GeometricAlgebra(3)  # a 3-D geometric algebra
    >>> locals().update(my_algebra.blades)   # add the basis blades to the locals (i.e. 1, e1, e2…)
    >>> reference_point = 0*e0           # the point of reference for the screw (here, the origin)
    >>> direction = 2 + (3*e1) + (6*e3)  # creates a MultiVector for the screw's direction
    >>> moment = (2*e1) + (5*e2) + e3    # creates another MultiVector for the screw's moment
    >>> my_screw = Screw(reference_point, direction, moment)  # finally we create a Screw instance
"""


class ScrewBase:
    """Provides a set of common methods for Screw and CoScrew classes.

    .. note::
        You can print a Screw directly by ``print(my_screw)`` but it is recommended to use the
        ``Screw.show`` method in order to have a better control on the reference point.

    Attributes
    ----------
    ref_point : MultiVector
        The point of reference of the screw.
    direction : MultiVector
        The direction multivector S or the screw.
    moment : MultiVector
        The moment multivector M of the the screw.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: change_point
    .. automethod:: show
    """
    classname = "ScrewBase"

    def __init__(self, ref_point, direction, moment):
        """Constructor method.

        Parameters
        ----------
        ref_point : MultiVector
            The point of reference of the (co)screw
        direction : MultiVector
            The direction of the (co)screw, usually named S.
        moment : MultiVector
            The moment of the (co)screw, usually named M.

        Raises
        ------
        TypeError
            If ``ref_point`` is not as point.
        """
        if ref_point(1) != ref_point:
            raise TypeError("ref_point is not a point")

        self.ref_point = ref_point
        self.direction = direction
        self.moment = moment

    def __repr__(self):
        """Allow to display the (co)Screw at its reference point.

        Returns
        -------
        out : str
            The string representation of the (co)Screw.
        """
        return f"{self.classname}(\n\tdirection={self.direction}\n\tmoment={self.moment}\n)"

    def change_point(self, new_point):
        """Computes and returns the (co)screw on the new reference point.

        Parameters
        ----------
        new_point : MultiVector
            The new point.

        Returns
        -------
        out : (co)Screw
            The (co)screw on ``new_point``.
        """
        return self.__class__(
                new_point,
                self.direction,
                self.moment - ((new_point - self.ref_point) ^ self.direction)
            )

    def show(self, new_point=None):
        """Print the (co)screw on a given point.

        Parameters
        ----------
        new_point : MultiVector, optionnal
            The point on which the (co)screw should be shown. If no point was given, it shows the
            (co)screw at its reference point.
        """
        if new_point is None:
            print(self)
        else:
            print(self.change_point(new_point))


class Screw(ScrewBase):
    """Screw object.

    The following operators have been overloaded:

    * the addition of screws
      ``self + other``

    * the right-handed addition
      ``other + self``

    * the outer product of screws
      ``self ^ other``

    See also
    --------
    This class inherits from the ScrewBase one.
    """
    classname = "Screw"

    def __add__(self, other):
        """The addition ``self + other``.

        Parameters
        ----------
        other : Screw
            The screw to be add up.

        Returns
        -------
        out : Screw
            The result of the addition of the two screws.

        Raises
        ------
        TypeError
            If ``other`` isn't a Screw.
        """
        if not isinstance(other, Screw):
            raise TypeError(f"other must be a Screw instance instead of {type(other)}")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return Screw(
                self.ref_point,
                self.direction + other.direction,
                self.moment + other.moment
            )

    __radd__ = __add__

    def __xor__(self, other):
        """The wedge product ``self ^ other``.
        
        Parameters
        ----------
        other : Screw
            The other Screw.

        Returns
        -------
        out : Screw
            The result of the wedge product between the two given screws.

        Raises
        ------
        TypeError
            If ``other`` isn't a Screw.
        """
        if not isinstance(other, Screw):
            raise TypeError(f"other must be a Screw instance instead of {type(other)}")

        if self.ref_point != other.ref_point:
            other = other.change_point(self.ref_point)

        return Screw(
                self.ref_point,
                (self.direction ^ other.moment) + (self.moment.grade_involution() ^
                        other.direction),
                self.moment ^ other.moment
            )


class CoScrew(ScrewBase):
    """Coscrew object

    The following operators have been overloaded:

    * the addition of coscrews
      ``self + other``

    * the right-handed addition
      ``other + self``

    * the product between a scalar and a coscrew
      ``scalar * self``

    See also
    --------
    This class inherits from the ScrewBase one.
    """
    classname = "CoScrew"

    def __add__(self, other):
        """The addition ``self + other``.

        Parameters
        ----------
        other : CoScrew
            The coscrew to be add up.

        Returns
        -------
        out : CoScrew
            The result of the addition of the two coscrews.

        Raises
        ------
        TypeError
            If ``other`` isn't a CoScrew.
        """
        if not isinstance(other, CoScrew):
            raise TypeError(f"other must be a CoScrew instance instead of {type(other)}")

        return CoScrew(
                self.ref_point,
                self.direction + other.direction,
                self.moment + other.moment
            )

    __radd__ = __add__

    def __rmul__(self, scalar):
        """The right-hand multiplication between a coscrew and a scalar ``scalar * self``.

        Parameters
        ----------
        scalar : int, float
            The scalar to multiply.

        Returns
        -------
        out : CoScrew
            The result of the addition of the two coscrews.

        Raises
        ------
        TypeError
            If ``scalar`` isn't a scalar.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"scalar must be a scalar instead of {type(scalar)}")

        return CoScrew(
                self.ref_point,
                scalar * self.direction,
                scalar * self.moment
            )

def comoment(coscrew: CoScrew, screw: Screw):
    """Compute the comoment between a coscrew and a screw.

    Parameters
    ----------
    coscrew : CoScrew
        The coscrew.
    screw : Screw
        The screw.

    Returns
    -------
    out : MultiVector
        The comoment between the given coscrew and the screw.
    """
    return (-coscrew.direction.grade_involution() * screw.moment.grade_involution()
            + screw.direction * coscrew.moment)(0)
