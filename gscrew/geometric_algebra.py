"""
Implements a MultiVector object and its basic manipulations. This module also provides a
GeometricAlgebra class to have a workspace for multivectors instance.

Classes
-------
.. autoclass:: GeometricAlgebra
.. autoclass:: MultiVector
"""
import itertools
import math
import numpy as np

class GeometricAlgebra:
    """Implements a geometric algebra of a given dimension.

    In most cases, you won't have to manipulate this object.

    Print a GeometricAlgebra instance will display the basis blades of the algebra.

    Attributes
    ----------
    dim : int
        The dimension of the algebra. This will create the basis blades of the algebra.
    nb_blades : int
        The number of basis blades the algebra has.
    blades_by_grade : list
        The number of basis blades per grade.
        e.g. for a 3D-algebra, it will be ``[1, 3, 3, 1]``
    blades_ids : list
        It contains the ids of the basis blades.
        e.g. for a 2D-algebra, the basis blades are: ``e0, e1, e2, e12`` so the ids will be:
        ``[(), (1,), (2,), (1, 2)]``.
    blades : dict
        This dictionnary contains the basis blades: ``{name: value}`` where
        ``name`` is a string (e.g. ``'e0'``, ``'e1'``, ``'e2'`` etc) and ``value`` the associated
        MultiVector instance.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: get_grade
    """
    def __init__(self, dim: int=3):
        """Constructor method.
        
        Parameters
        ----------
        dim : int, optionnal
            The wanted dimension if the geometric algebra. By default, this will generate a three
            dimensional one. 
        """
        self.dim = dim
        self.nb_blades = 2 ** dim

        self.blades_by_grade = [binomial_coefficient(dim, i) for i in range(dim + 1)]

        ids = []
        for i in range(self.nb_blades):
            ids.append((to_array(i, dim), i.bit_count(), i))

        self.blades_ids = [i[0] for i in sorted(ids, key=lambda x: x[1])]

        self.blades = {}
        self.__generate_blades()

    def __repr__(self):
        """Returns the string representation of the geometric algebra.

        Returns
        -------
        out : str
            The string representation of the algebra.
        """
        return str(list(self.blades.values()))

    def __generate_blades(self):
        """Generate the basis blades for the given dimension."""
        ids = [i + 1 for i in range(self.dim)]
        blades_names = list(itertools.chain.from_iterable(
                itertools.combinations(ids, r)
                for r in range(self.dim + 1)
            ))

        names = []
        for index, blade_name in enumerate(blades_names):
            if index:
                names.append("e" + "".join(map(str, blade_name)))
            else:
                names.append("e0")

        value = np.zeros(self.nb_blades)
        for i in range(self.nb_blades):
            value[i] = 1
            self.blades[names[i]] = MultiVector(self, value)
            value[i] = 0

    def get_grade(self, grade: int):
        """Returns the first and the last index of the researched grade. It can be useful if you
        search all the k-vectors of a given algebra, then you give the grade (i.e. k) and this
        method will return you the index of the first k-vector and the index of the last k-vector of
        your algebra.

        Parameters
        ----------
        grade : int
            The grade you are searching for.

        Returns
        -------
        out : tuple
            The output is a tuple composed of two elements. The first one is the first index and the
            second one, the last.

        Exemples
        --------
        If we work in a three-dimensionnal algebra::

            >>> geo_alg = ga.GeometricAlgebra(3)
            >>> geo_alg.get_grade(2)
            (4, 6)

        Indeed, the first bivector (i.e. e12) is at index 4 and the last one (i.e. e23) is at 6.
        """
        first_index = sum(self.blades_by_grade[:grade])
        last_index = first_index + self.blades_by_grade[grade]
        return first_index, last_index - 1


class MultiVector:
    """An element of the geometric algebra.

    The following operators have been overloaded:

    * the addition
      ``self + other``

    * the substraction
      ``self - other``

    * the geometric product
      ``self * other``

    * the outer product
      ``self ^ other``

    * the inner product
      ``self | other``

    Attributes
    ----------
    geo_alg : GeometricAlgebra
        The geometric algebra to which the multivector belongs.
    value : np.array
        The coefficients on each basis blade.

    Methods
    -------
    .. automethod:: __init__
    .. automethod:: __call__
    .. automethod:: __getitem__
    .. automethod:: norm
    .. automethod:: grade_involution

    Exemples
    --------
    Let's show you a complete exemple of a manipulation of MultiVector.
    You must start by importing the module::

        >>> import geometric_algebra as ga
        >>> geo_alg = ga.GeometricAlgebra(3)  # you should give the dimension of the algebra
        >>> locals().update(geo_alg.blades)   # import the basis blades e.g. e0, e1, e2, e3, e12 etc

    Then you have fully initialize the module. To create a new MultiVector instance, you have two
    possibilities. The first one is also the easiest::

        >>> my_mv = 1 + 1*e1 + 5*e2 + (1/5) * e13

    You can also call the constructor method manually::
        
        >>> my_mv = ga.MultiVector(geo_alg, (1, 1, 5, 0, 0, 1/5, 0, 0))

    .. warning::
        In the second case you have to give all the coefficients and the GeometricAlgebra instance.

    .. note::
        When you just create a new MultiVector by using the basis blades, the new instance inherits
        the geometric algebra of the basis blades.
    """
    def __init__(self, geo_alg: GeometricAlgebra, value=None):
        """Constructor method.

        Parameters
        ----------
        geo_alg : GeometricAlgebra
            The algebra to which the multivector belongs.
        value
            The coefficients of the multivector.

            .. note:: It must be transtypable into an np.array.
        """
        self.geo_alg = geo_alg
        if value is None:
            self.value = np.zeros(geo_alg.nb_blades)
        else:
            if isinstance(value, (int, float)):
                new_value = np.zeros(geo_alg.nb_blades)
                new_value[0] = value
            else:
                new_value = np.array(value)
            self.value = new_value

    def __add__(self, other):
        """Compute the addition ``self + other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to add up.

        Returns
        -------
        out : MultiVector
            The result of the addition.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = self.value.copy()
        if isinstance(other, (int, float)):
            new_value[0] += other

        elif isinstance(other, MultiVector):
            new_value += other.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __call__(self, *grades):
        """Project the multivector on the basis blades of given grades.

        Parameters
        ----------
        *grades
            The grades on which the multivector will be project.

        Returns
        -------
        out : MultiVector
            The result of the projection.

        Exemples
        --------
        Let ``my_mv`` be a multivector such that ``my_mv = 1 + (2^e1) + (3^e2) + (4^e12)`` and let's
        see some projections::

            >>> my_mv = 1 + (2^e1) + (3^e2) + (4^e12)
            >>> my_mv(0)  # projection on scalar
            1
            >>> my_mv(1)  # projection on vectors
            (2^e1) + (3^e2)
            >>> my_mv(0, 2)  # projection on scalar and bivectors
            1 + (4^e12)
        """
        new_value = np.zeros(self.geo_alg.nb_blades)
        for grade in grades:
            first_index, last_index = self.geo_alg.get_grade(grade)
            for index in range(first_index, last_index + 1):
                new_value[index] = self.value[index]
        return MultiVector(self.geo_alg, new_value)

    def __eq__(self, other):
        """Test the equality between two multivectors.

        Parameters
        ----------
        other : MultiVector
            The other multivector.

        Returns
        -------
        out : bool
            This method will return ``True`` if all the components of the two multivectors are
            equals. 
        """
        if isinstance(other, (int, float)):
            return self[0] == other
        return (self.value == other.value).all()

    def __getitem__(self, index: int):
        """Returns the component at the given index.

        Parameters
        ----------
        index : int
            The index of the desired component.

        Returns
        -------
        out : float
            The desired component.
        """
        return self.value[index]

    def __mul__(self, other):
        """Compute the geometrical product ``self * other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the geometrical product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if isinstance(other, (int, float)):
            return MultiVector(self.geo_alg, self.value * other)

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        new_value = np.zeros(self.geo_alg.nb_blades)
        for i in range(self.geo_alg.nb_blades):
            if self[i]:
                for j in range(self.geo_alg.nb_blades):
                    if other[j]:
                        index, sgn = self.__mul_basis(i, j)
                        new_value[index] += sgn * self[i] * other[j]

        return MultiVector(self.geo_alg, new_value)

    def __neg__(self):
        """Unary minus ``-self``.

        Returns
        -------
        out : MultiVector
            The opposed MultiVector.
        """
        return MultiVector(self.geo_alg, -self.value.copy())

    def __or__(self, other):
        """Compute the inner product ``self | other``.

        Parameters
        ----------
        other : MultiVector
            The other MultiVector.

        Returns
        -------
        out : MultiVector
            The result of the inner product.

        Raises
        ------
        TypeError
            If ``other`` isn't a MultiVector instance.
        """
        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )
        return sum(self.value * other.value)

    __radd__ = __add__

    def __repr__(self):
        """Returns the string representation of the MultiVector.

        Returns
        -------
        string : str
            The string representation of the MultiVector.
        """
        string = ""
        blades_names = tuple(self.geo_alg.blades.keys())
        for index, coeff in enumerate(self.value):
            if coeff:
                if coeff > 0 and string:
                    string += " + "
                if coeff < 0:
                    string += " - "
                if index:
                    string += f"({abs(coeff)}^{blades_names[index]})"
                else:
                    string += f"{abs(coeff)}"

        if not string:
            return "0"
        return string.strip()

    def __rmul__(self, other):
        """Compute the right-hand geometrical product ``other * self``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the geometrical product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if isinstance(other, (int, float)):
            return MultiVector(self.geo_alg, other * self.value)

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        new_value = np.zeros(self.geo_alg.nb_blades)
        for i in range(self.geo_alg.nb_blades):
            if other[i]:
                for j in range(self.geo_alg.nb_blades):
                    if self[j]:
                        index, sgn = self.__mul_basis(j, i)
                        new_value[index] += sgn * other[i] * self[j]

        return MultiVector(self.geo_alg, new_value)

    def __rsub__(self, other):
        """Compute the subtraction ``other - self``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to subtract.

        Returns
        -------
        out : MultiVector
            The result of the subtraction.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = np.zeros(self.geo_alg.nb_blades)
        if isinstance(other, (int, float)):
            new_value[0] = other - self.value[0]
            new_value[1:] -= self.value[1:]

        elif isinstance(other, MultiVector):
            new_value = other.value.copy()
            new_value -= self.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __rxor__(self, other):
        """Compute the right-hand outer product ``other ^ self``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the outer product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if isinstance(other, (int, float)):
            return other * self

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        if self == other:
            return MultiVector(self.geo_alg)
        return (other * self) - (other | self)

    __str__ = __repr__

    def __sub__(self, other):
        """Compute the subtraction ``self - other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to subtract.

        Returns
        -------
        out : MultiVector
            The result of the subtraction.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        new_value = self.value.copy()
        if isinstance(other, (int, float)):
            new_value[0] -= other

        elif isinstance(other, MultiVector):
            new_value -= other.value

        else:
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        return MultiVector(self.geo_alg, new_value)

    def __xor__(self, other):
        """Compute the outer product ``self ^ other``.

        Parameters
        ----------
        other : MultiVector, scalar
            The MultiVector or scalar to multiply.

        Returns
        -------
        out : MultiVector
            The result of the outer product.

        Raises
        ------
        TypeError
            If ``other`` is neither a scalar nor a MultiVector instance.
        """
        if isinstance(other, (int, float)):
            return self * other

        if not isinstance(other, MultiVector):
            raise TypeError(f"other must be a scalar or a MultiVector instance instead of "\
                    f"{type(other)}"
                )

        if self == other:
            return MultiVector(self.geo_alg)
        return (self * other) - (self | other)

    def __mul_basis(self, index1: int, index2: int):
        """Compute the geometrical product between two basis blades.

        Parameters
        ----------
        index1 : int
            The first basis blade (its index).
        index2 : int
            The second basis blade (its index).

        Returns
        -------
        out : tuple
            A tuple of the form: ``(index, sign)`` where ``index`` is the index of the
            resulting basis blade and ``sign`` the sign of the result.
        """
        array = [
                i^j for i, j in
                zip(self.geo_alg.blades_ids[index1], self.geo_alg.blades_ids[index2])
            ]

        new_index = self.geo_alg.blades_ids.index(array)
        sign = get_sign(self.geo_alg.blades_ids[index1], self.geo_alg.blades_ids[index2])
        return new_index, sign

    def copy(self):
        """Create a deep copy of the instance.

        Returns
        -------
        out : MultiVector
            The copy of the instance.
        """
        return MultiVector(self.geo_alg, self.value.copy())

    def norm(self):
        """Compute the norm of the multivector.

        Returns
        -------
        out : float
            The norm of the multivector"""
        result = 0
        for component in self.value:
            result += abs(component ** 2)

        return math.sqrt(result)

    def grade_involution(self):
        """Compute the grade involution of the multivector.

        Returns
        -------
        new_mv : MultiVector
            The result of the grade involution.
        """
        new_mv = MultiVector(self.geo_alg)
        for i in range(self.geo_alg.dim + 1):
            new_mv += (-1)**i * self(i)
        return new_mv


def binomial_coefficient(n: int, k: int):
    """Compute the binomial coefficient nCk.
    
    Parameters
    ----------
    n : int
        The first integer.
    k : int
        The second integer

    Returns
    -------
    coeff : int
        The binomial coefficient: nCk.
    """
    if k < 0 or k > n:
        return 0
    if k in (0, n):
        return 1
    k = min(k, n - k)

    coeff = 1
    for i in range(k):
        coeff = coeff * (n - i) // (i + 1)

    return coeff

def to_array(integer: int, nb_bit: int):
    """Convert an integer into an array of bits.

    Parameters
    ----------
    integer : int
        The integer to convert into an array.
    nb_bit : int
        The number of bits over which to express ``integer``.

    Returns
    -------
    array : np.array
        The array of bits.

    Raises
    ------
    ValueError
        If the integer can't be expressed on ``nb_bit`` bits.

    Exemples
    --------
    For exemple, the decimal number 5 is expressed as 101 in base 2, if we want to have an array of
    4 bits, the function will return ``np.array([0, 1, 0, 1])``::

        >>> to_array(5, 4)
        array([0, 1, 0, 1])
        >>> to_array(7, 3)
        array([1, 1, 1])
    """
    if integer >= 2 ** nb_bit:
        raise ValueError(f"{integer} can't be expressed on {nb_bit} bits")

    array = list(map(int, bin(integer)[2:]))
    while len(array) < nb_bit:
        array.insert(0, 0)
    return array


def get_index(array_like, search_element: np.array):
    """Search the index of ``search_element`` into ``array_like``.

    Parameters
    ----------
    array_like
        A list or a tuple of NumPy arrays.
    search_element : np.array
        The researched array

    Returns
    -------
    index : int
        The index of ``search_element`` in ``array_like``.

    Raises
    ------
    ValueError
        If ``search_element`` is not in ``array_like``.
    """
    return np.where(search_element == array_like)

    # for index, value in enumerate(array_like):
    #     if (value == search_element).all():
    #         return index
    # raise ValueError(f"{rslt} not in {array_like.__class__.__name__}")


def get_sign(array1: np.array, array2: np.array):
    """Calculate the sign of the geometric product between the given basis blades.

    Parameters
    ----------
    array1 : np.array
        The array form of the first basis blade.
    array2 : np.array
        The array form of the second basis blade.

    Returns
    -------
    out : int
        The sign of the geometric product between the two basis blades.
    """    
    id1 = int("0b" + "".join(map(str, array1)), 2) // 2
    id2 = int("0b" + "".join(map(str, array2)), 2)

    n_swap = 0
    while id1:
        n_swap += (id1 & id2).bit_count()
        id1 //= 2
    n_swap += 1
    return 2 * (n_swap % 2) - 1
