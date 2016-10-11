import tkinter as tk
import itertools
import math
from point import Point, Vector


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800

COLOURS = ['gold', 'light sky blue', 'firebrick']
ARC_COLOURS = COLOURS

ARC_SIZE = .3


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

    def draw_napoleons_theorem(self):
        outer_centres = []

        # Draw equilaterals
        for i, colour in enumerate(COLOURS):
            p1, p2, orientator = [self._points[(i + j) % len(self._points)] for
                                  j in range(3)]
            p3 = self.generate_equilateral(p1, p2, orientator)
            p3 = Point(*p3)

            # Calculate centre and store it
            centre = self.calculate_equilateral_centre(p1, p2, p3)
            outer_centres.append(centre)

            # side equilateral
            sprite = self._canvas.create_polygon(tuple(p1), tuple(p2),
                                                 tuple(p3),
                                                 fill=colour, outline='black')

            # lines to centre of side equilateral
            self._canvas.create_line(tuple(p1), tuple(centre), dash=(5,5))
            self._canvas.create_line(tuple(p2), tuple(centre), dash=(5,5))

        self._canvas.create_polygon(*(tuple(p) for p in outer_centres), fill='',
                                    outline='black')

    def calculate_equilateral_centre(self, p1, p2, p3):
        """
        Returns the centre point of an equilateral triangle.
        :param p1: First corner. Instance of Point or iterable.
        :param p2: Second corner. Instance of Point or iterable.
        :param p3: Third corner. Instance of Point or iterable.
        :return: Point instance with centre coordinates.
        """

        dp = p2 - p1

        invert = (p1 - p3).determinant(p2 - p3) > 0

        if invert:
            theta1 = math.pi / 6
            theta2 = -math.pi / 6
        else:
            theta1 = -math.pi / 6
            theta2 = math.pi * 7 / 6

        v1 = dp.rotate(theta1)
        v2 = (-dp).rotate(theta2)

        l1 = Vector(p1, v1)
        l2 = Vector(p2, v2)

        return l1.intersects2d(l2)

    def draw_moreleys_miracle(self):
        # Draw arcs
        inner_trisections = []
        for i, colour in enumerate(ARC_COLOURS):

            p1, p2, p3 = [self._points[(i + j) % len(self._points)] for
                          j in range(3)]

            side1 = p3.distance(p1)
            side2 = p3.distance(p2)
            side = min(side1, side2)
            r = side * ARC_SIZE

            x, y = p3
            v1 = p1 - p3
            v2 = p2 - p3

            a1 = -math.atan2(v1[1], v1[0])
            extent = v2.angle_between(v1)

            d = v1.determinant(v2)
            if d > 0:
                extent = -extent

            for i in range(1, 3):
                inner_trisections.append((p3, a1 + extent * i / 3))

            self._canvas.create_arc(x - r, y - r, x + r, y + r,
                                    start=math.degrees(a1),
                                    extent=math.degrees(extent), fill=colour)

        # Draw trisections of inner angles
        inner_points = []

        for i in range(3):
            p1, theta1 = inner_trisections[i]
            p2, theta2 = inner_trisections[i + 3]
            colour = COLOURS[(2 - i) % 3]

            v1, v2 = [Point.from_polar(-theta, 200) for theta in
                      (theta1, theta2)]

            l1 = Vector(p1, v1)
            l2 = Vector(p2, v2)

            p3 = l1.intersects2d(l2)
            inner_points.append(p3)
            p3 = tuple(p3)

            [self._canvas.create_line(p3, tuple(p), fill=colour) for p in
             (p1, p2)]

        # Draw inner triangle
        self._canvas.create_polygon(*(tuple(p) for p in inner_points),
                                    fill='white', outline='black')

        # Draw extension
        # TODO: clean up and use symmetry to make more efficient

        outer_trisections = [[], []]

        for i in range(3):
            p1, p2, p3 = [self._points[(i + j) % len(self._points)] for
                          j in range(3)]

            v1 = p1 - p3
            v2 = p2 - p3

            # extend edges
            self._canvas.create_line(tuple(p1), tuple(p1 - 100 * v1), dash=(5, 5))
            self._canvas.create_line(tuple(p2), tuple(p2 - 100 * v2), dash=(5, 5))

            d = v1.determinant(v2)

            theta = v1.angle_between(-v2)

            if d < 0:
                theta = -theta

            line_colours = ['red', 'blue']

            for i, colour in zip(range(1, 3), line_colours):

                outer_trisections[i-1].append((p3, v1.rotate(-theta*i/3)))
                outer_trisections[i-1].append((p3, v2.rotate(+theta*i/3)))


        colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

        # closer trisection
        outer_closest_tips = []
        for i in range(3):
            colour_i = (6- 2*i + 3) % 6
            colour = colours[colour_i]
            p1, v1 = outer_trisections[0][i]
            p2, v2 = outer_trisections[0][i+3]

            l1 = Vector(p1, v1)
            l2 = Vector(p2, v2)

            p3 = l1.intersects2d(l2)

            outer_closest_tips.append(p3)

            # Draw trisection lines
            self._canvas.create_line(tuple(p1),
                                     tuple(p1 + 100 * v1), dash=(5, 5),
                                     fill=colour)

            self._canvas.create_line(tuple(p2),
                                     tuple(p2 + 100 * v2), dash=(5, 5),
                                     fill=colour)

        # Draw inner triangle
        self._canvas.create_polygon(*(tuple(p) for p in outer_closest_tips),
                                    fill='', outline='black')

        outer_other_tips = []



        for i, j in zip(range(6), itertools.cycle((4,2))):
            colour = colours[(((i+1)//2)*2 + 1)%6]

            i_t = inner_trisections[(i+j)%6]
            o_t = outer_trisections[1][i]

            i_p, i_theta = i_t
            i_v = Point.from_polar(-i_theta)
            o_p, o_v = o_t

            l1 = Vector(i_p, i_v)
            l2 = Vector(o_p, o_v)

            p = l1.intersects2d(l2)

            self._canvas.create_line(tuple(i_p), tuple(p), fill=colour, dash=(5,5))
            self._canvas.create_line(tuple(o_p), tuple(p), fill=colour, dash=(5,5))

            outer_other_tips.append(p)

        for i in range(3):
            p1 = outer_closest_tips[i]
            p2 = outer_other_tips[i]
            p3 = outer_other_tips[i+3]

            colour = COLOURS[(2 - i)%3]

            self._canvas.create_polygon(tuple(p1), tuple(p2), tuple(p3), fill=colour, outline='black')



    def draw(self):
        self._canvas.delete(tk.ALL)
        self._canvas.create_polygon(*(tuple(p) for p in self._points), fill='white', outline='black')
        self.draw_moreleys_miracle()
        #self.draw_napoleons_theorem()


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
