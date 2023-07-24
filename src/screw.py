"""
This module provides two classes that respectively implement a screw and a co-screw.

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
    >>> direction = 2 + (3*e1) + (6*e3)      # creates a MultiVector for the screw's direction
    >>> moment = (2*e1) + (5*e2) + e3        # creates another MultiVector for the screw's moment
    >>> my_screw = Screw(direction, moment)  # finally we create a Screw instance
"""


class Screw:
    """Screw object

    Attributes
    ----------
    direction : MultiVector
        The direction multivector S or the screw.
    moment : MultiVector
        The moment multivector M of the the screw.
    """
    def __init__(self, direction, moment):
        """Constructor method.

        Parameters
        ----------
        direction : MultiVector
            The direction of the screw, usually named S.
        moment : MultiVector
            The moment of the screw, usually named M.
        """
        self.direction = direction
        self.moment = moment

    def __repr__(self):
        """Allow to display the Screw.

        Returns
        -------
        out : str
            The string representation of the Screw.
        """
        return f"Screw(\n\tdirection={self.direction}\n\tmoment={self.moment}\n)"

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

        return Screw(
                self.direction + other.direction,
                self.moment + other.moment
            )

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

        return Screw(
                self.direction ^ other.moment + self.moment.grade_involution() ^ other.direction,
                self.moment ^ other.moment
            )


class CoScrew:
    """Coscrew object

    Attributes
    ----------
    direction : MultiVector
        The direction multivector S or the coscrew.
    moment : MultiVector
        The moment multivector M of the the coscrew.
    """
    def __init__(self, direction, moment):
        """Constructor method.

        Parameters
        ----------
        direction : MultiVector
            The direction of the screw, usually named S.
        moment : MultiVector
            The moment of the screw, usually named M.
        """
        self.direction = direction
        self.moment = moment

    def __repr__(self):
        """Allow to display the CoScrew.

        Returns
        -------
        out : str
            The string representation of the CoScrew.
        """
        return f"CoScrew(\n\tdirection={self.direction}\n\tmoment={self.moment}\n)"

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
                self.direction + other.direction,
                self.moment + other.moment
            )

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
            + screw.direction * coscrew.moment)
