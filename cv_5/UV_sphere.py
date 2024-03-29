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


center = (0, 0)
radius = 5

num_meridians = 10
num_parallels = 10


def generate_sphere_points():
    """Generates a UV sphere."""
    return_points = []

    # Generate the top point
    return_points.append([Point(0, 0, radius, 0)])

    num = 1
    for i in range(1, num_parallels+1):
        theta = pi/2 + i/(num_parallels+1) * pi
        z = radius * sin(theta)
        parallels = []
        for j in range(num_meridians):
            gamma = j/num_meridians * 2*pi
            x = radius * cos(theta) * cos(gamma)
            y = radius * cos(theta) * sin(gamma)
            parallels.append(Point(round(x, 5), round(y, 5), round(z, 5), num))
            num += 1

        return_points.append(parallels)

    # Generate the bottom point
    return_points.append([Point(0, 0, -radius, num)])

    return return_points


def export_vtk(points, filename):
    """Export the points, which represent a sphere into a vtk file."""

    header = '# vtk DataFile Version 3.0\nIHLAN example\nASCII\nDATASET POLYDATA\n'

    file = open(filename, 'w')
    file.write(header)

    # Count the number of points
    num_points = 0
    for parallel in points:
        num_points += len(parallel)

    # Write points
    file.write(f'POINTS {points[-1][-1].i + 1} float\n')
    for parallel in points:
        for point in parallel:
            file.write(f'{point.x} {point.y} {point.z}\n')

    # Count the number of triangles
    num_triangles = 2 * (len(points) - 2) * len(points[1])

    # Write triangles
    file.write(f'POLYGONS {num_triangles} {num_triangles*4}\n')

    # Write the top row
    for i, row in enumerate(points):
        # Skip the top point
        if i == 0:
            continue

        # Something special if generating the first row, because the first
        # row is just one point
        if i == 1:
            for j, point in enumerate(row[:-1]):
                file.write(
                    f'3 {points[i][j].i} {points[i][j+1].i} {points[i-1][0].i}\n')
            file.write(
                f'3 {points[i][j+1].i} {points[i][0].i} {points[i-1][0].i}\n')
            continue

        # Something special if generating the last row, because the last
        # row is just one point
        if i == len(points)-1:
            for j, point in enumerate(points[i-1][:-1]):
                file.write(
                    f'3 {points[i-1][j].i} {points[i][0].i} {points[i-1][j+1].i}\n')
            file.write(
                f'3 {points[i-1][j+1].i} {points[i][0].i} {points[i-1][0].i}\n')
            continue

        # If you got this far, just the normal case
        for j, point in enumerate(row[:-1]):
            file.write(
                f'3 {points[i][j].i} {points[i][j+1].i} {points[i-1][j+1].i}\n')
            file.write(
                f'3 {points[i][j].i} {points[i-1][j+1].i} {points[i-1][j].i}\n')
        file.write(
            f'3 {points[i][j+1].i} {points[i][0].i} {points[i-1][0].i}\n')
        file.write(
            f'3 {points[i][j+1].i} {points[i-1][0].i} {points[i-1][j+1].i}\n')

    file.close()


if __name__ == '__main__':
    points = generate_sphere_points()
    export_vtk(points, 'UVShere.vtk')
