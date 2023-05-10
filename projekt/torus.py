"""Code for generating a UV sphere, export a vtk for visualization."""


from math import sin, cos, pi


class Point:
    def __init__(self, x, y, z, i):
        self.x = x
        self.y = y
        self.z = z
        self.i = i

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Polygon:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return f'({self.points})'


main_radius = 5
radius = 1

num_x = 10
num_y = 10


def generate_sphere_points():
    """Generates a UV sphere."""
    points = [[Point(0, 0, 0, y*num_x + x)
               for x in range(num_x)] for y in range(num_y)]

    for x in range(num_x):
        for y in range(num_y):
            alfa = 2 * pi * x / num_x
            beta = 2 * pi * y / num_y
            points[x][y].x = (main_radius + radius * sin(beta)) * cos(alfa)
            points[x][y].y = (main_radius + radius * sin(beta)) * sin(alfa)
            points[x][y].z = radius * cos(beta)

    polygons = []

    for y in range(num_y):
        for x in range(num_x):
            polygons.append(
                Polygon([
                    points[y][x].i,
                    points[y][(x+1) % num_x].i,
                    points[(y+1) % num_y][(x+1) % num_x].i,
                ]))
            polygons.append(
                Polygon([
                    points[y][x].i,
                    points[(y+1) % num_y][(x+1) % num_x].i,
                    points[(y+1) % num_y][x].i,
                ]),
            )

    return (points, polygons)


def export_vtk(points, polygons, filename):
    """Export the points, which represent a sphere into a vtk file."""

    header = '# vtk DataFile Version 3.0\nIHLAN example\nASCII\nDATASET POLYDATA\n'

    file = open(filename, 'w')
    file.write(header)

    # Write points
    file.write(f'POINTS {points[-1][-1].i + 1} float\n')
    for row in points:
        for point in row:
            file.write(f'{point.x} {point.y} {point.z}\n')

    # Count the number of triangles
    num_triangles = 2 * num_x * num_y

    # Write triangles
    file.write(f'POLYGONS {num_triangles} {num_triangles*4}\n')

    for polygon in polygons:
        file.write(
            f'3 {polygon.points[0]} {polygon.points[1]} {polygon.points[2]}\n')


if __name__ == '__main__':
    (points, polygons) = generate_sphere_points()
    export_vtk(points, polygons, 'torus.vtk')
