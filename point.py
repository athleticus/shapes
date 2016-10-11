from numbers import Number
import math

class Point:
    """
    Represents an n-dimensional point/vector.

    Point is often treated as a vector, and has many relevant methods.

    TODO: unary ops, normal/reflected arithmetic ops
    """

    __slots__ = ['_coords']

    def __init__(self, *coords):
        """
        Constructs Point with dimensions equal to number of coordinates.
        """
        self._coords = tuple(coords)

    def __repr__(self):
        return "Point{!r}".format(self._coords)

    def __iter__(self):
        return iter(self._coords)

    def __getitem__(self, item):
        return self._coords[item]

    def __len__(self):
        return len(self._coords)

    def __pos__(self):
        raise NotImplementedError

    def __neg__(self):
        return Point(*(-x for x in self._coords))

    def __abs__(self):
        raise NotImplementedError
    def __invert__(self):
        raise NotImplementedError
    def __round__(self, n):
        raise NotImplementedError
    def __floor__(self):
        raise NotImplementedError
    def __ceil__(self):
        raise NotImplementedError
    def __trunc__(self):
        raise NotImplementedError

    def __add__(self, other):
        return Point(*(x + y for x, y in zip(self._coords, other._coords)))

    def __sub__(self, other):
        return Point(*(x - y for x, y in zip(self._coords, other._coords)))

    def __mul__(self, other):
        if isinstance(other, Number):
            return Point(*(x * other for x in self._coords))
        elif isinstance(other, Point):
            return Point(*(x * y for x, y in zip(self._coords, other._coords)))
        else:
            raise TypeError("Unsupported type.")

    # Multiplication is commutative
    __rmul__ = __mul__
    # def __rmul__(self, other):
    #     return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        return Point(*(x ** power for x in self._coords))

    def distance(self, other):
        return sum([(x - y) ** 2 for x, y in zip(self._coords, other._coords)]) ** 0.5

    def angle_between(self, other):
        """
        Returns the angle between two vectors.

        :param other: Other vector (instance of Point).
        :return: Angle between self & other in radians.
        """

        return math.acos(self.dot(other)/(self.length() * other.length()))

    def angle(self):
        """
        Returns the angle between this vector and positive x-axis.

        :param other: Other vector (instance of Point).
        :return: Angle between self & other in radians.
        """
        return self.angle_between(Point(0, 1))

    def length(self):
        """
        Returns the length of this vector.

        :return: float
        """
        return sum([x ** 2 for x in self._coords]) ** 0.5

    def __float__(self):
        """
        :return: Length of vector.
        """
        return self.length()

    def dot(self, other):
        """
        Returns the dot product of two vectors.

        :param other:
        :return:
        """
        return sum(self * other)

    def determinant(self, other):
        if len(self) != 2 or len(other) != 2:
            raise ValueError("Cannot take determinant of non-2d vectors.")

        x1, y1 = self._coords
        x2, y2 = other._coords

        return x1 * y2 - x2 * y1

    @classmethod
    def from_polar(cls, r, angle):
        x = r * math.cos(angle)
        y = r * math.sin(angle)

        return Point(x, y)

class Vector:
    __slots__ = ['_point', '_direction']

    def __init__(self, point, direction):
        self._point = point
        self._direction = direction

    @classmethod
    def from_direction(cls, direction):
        point = Point(tuple(0 for i in range(len(direction))))
        return Vector(point, direction)

    def intersects2d(self, other):
        m1, c1 = self.to_scalar()
        m2, c2 = other.to_scalar()

        x = (c1 - c2)/(m2 - m1)
        y = m1 * x + c1

        return Point(x, y)

    def to_scalar(self):
        x0, y0 = self._point
        vx, vy = self._direction

        m = vy/vx
        c = y0 - m * x0

        return m, c

    def __repr__(self):
        return "Vector({!r}, {!r})".format(self._point, self._direction)





def main():
    p1 = Point(3, 4)
    p2 = Point(1,2)
    print(sum((p1 - p2)**2) ** 0.5)
    print(p1.distance(p2))
    print(p1 ** 2)
    print(tuple(p1))

    print(p1 * 5)
    print(5.5 * p1)

    print(p1.length())

    l1 = Vector(Point(1,3), (1,1))
    l2 = Vector(Point(4,2), (-1,1))

    print(l1.intersects2d(l2))

if __name__ == "__main__":
    main()

