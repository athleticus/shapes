import tkinter as tk
import itertools
import math
from point import Point, Vector


DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600

COLOURS = ['gold', 'light sky blue', 'firebrick']
ARC_COLOURS = COLOURS


def euclidean_distance(a, b):
    ax, ay = a
    bx, by = b

    return ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5



class TriangleApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._canvas = tk.Canvas(self, width=DEFAULT_WIDTH,
                                 height=DEFAULT_HEIGHT)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.bind('<Configure>', self._resize)
        self._canvas.bind('<Button-1>', self._click)
        self._canvas.bind('<B1-Motion>', self._drag)

        self._points = None

    def _click(self, ev):
        self._index, _ = min(enumerate(self._points),
                             key=lambda pair: euclidean_distance(pair[1],
                                                                 (ev.x, ev.y)))

        #print("Closest point is {}".format(self._points[self._index]))

        self.draw()

    def _drag(self, ev):
        self._points[self._index] = Point(ev.x, ev.y)

        self.draw()

    def draw(self):
        self._canvas.delete(tk.ALL)
        self._canvas.create_polygon(*(tuple(p) for p in self._points), fill='white')

        outer_centres = []

        # Draw equilaterals
        for i, colour in enumerate(COLOURS):
            p1, p2, orientator = [self._points[(i + j) % len(self._points)] for
                                  j in range(3)]
            p3 = self.generate_equilateral(p1, p2, orientator)
            p3 = Point(*p3)

            d1 = p3-p1
            a1 = math.atan2(d1[1], d1[0]) + math.pi/6

            d2 = p3-p2
            a2 = math.atan2(d2[1], d2[0]) - math.pi/6

            print(a1, a2)


            l1 = Vector(p1, Point.from_polar(200, a1))
            l2 = Vector(p2, Point.from_polar(200, a2))

            print(l1, l2)

            centre = l1.intersects2d(l2)
            outer_centres.append(centre)

            sprite = self._canvas.create_polygon(tuple(p1), tuple(p2), tuple(p3),
                                                 fill=colour, outline='black')



        self._canvas.create_polygon(*(tuple(p) for p in outer_centres), fill='', outline='black')

        # Draw arcs
        arc_size = 0.3

        trisections = []

        for i, colour in enumerate(ARC_COLOURS):

            p1, p2, p3 = [self._points[(i + j) % len(self._points)] for
                          j in range(3)]

            side1 = p3.distance(p1)
            side2 = p3.distance(p2)
            side = min(side1, side2)
            r = side * arc_size

            x, y = p3
            v1 = p1 - p3
            v2 = p2 - p3

            a1 = math.atan2(*(v1)) - math.pi / 2
            extent = v2.angle_between(v1)

            d = v2.determinant(v1)
            if d < 0:
                extent = -extent

            for i in range(1, 3):
                trisections.append((p3, a1 + extent * i / 3))

            self._canvas.create_arc(x - r, y - r, x + r, y + r,
                                    start=math.degrees(a1),
                                    extent=math.degrees(extent), fill=colour)

        # Draw trisections of inner angles
        inner_points = []

        for i in range(3):
            p1, theta1 = trisections[i]
            p2, theta2 = trisections[i + 3]
            colour = COLOURS[(2 - i) % 3]

            v1, v2 = [Point.from_polar(200, -theta) for theta in (theta1, theta2)]

            l1 = Vector(p1, v1)
            l2 = Vector(p2, v2)

            p3 = l1.intersects2d(l2)
            inner_points.append(p3)
            p3 = tuple(p3)

            [self._canvas.create_line(p3, tuple(p), fill=colour) for p in (p1, p2)]


        # Draw inner triangle
        self._canvas.create_polygon(*(tuple(p) for p in inner_points), fill='white', outline='black')


    def generate_equilateral(self, p1, p2, orientator, toward_orientator=False):
        """
        Draws an equilateral on p1->p2.

        :param p1: Point 1 on the equilateral triangle.
        :param p2: Point 2 on the equilateral triangle.
        :param orientator: Orientation point on the equilateral triangle.
        :param toward_orientator: If True, third point on equilateral is drawn
                                  toward orientator point. Defaults to False.

        :return: Point 3 on the equilateral triangle.
        """

        p1x, p1y = p1
        p2x, p2y = p2

        dx, dy = p2x - p1x, p2y - p1y

        r = euclidean_distance((dx, dy), (0, 0))
        theta = math.atan2(dy, dx)

        candidates = []

        for dtheta in (math.pi / 3, -math.pi / 3):
            dx = r * math.cos(theta + dtheta)
            dy = r * math.sin(theta + dtheta)

            point = p1x + dx, p1y + dy

            distance = euclidean_distance(point, orientator)

            candidates.append((distance, point))

        candidates.sort()
        if toward_orientator:
            candidates.reverse()
        p3 = candidates[1][1]

        return p3

    def _resize(self, ev):
        if self._points is None:
            width = ev.width
            height = ev.height
            self._points = [Point(int(x), int(y)) for x, y in [
                (226 / 600 * width, 177 / 600 * height),
                (427 / 600 * width, 293 / 600 * height),
                (154 / 600 * width, 316 / 600 * height)
            ]]

        self.draw()


def main():
    root = tk.Tk()
    TriangleApp(root).pack(expand=True, fill=tk.BOTH)
    root.mainloop()


if __name__ == "__main__":
    main()
