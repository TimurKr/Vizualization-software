"""Code for generating an IHLAN, export a vtk file for visualization."""

from math import cos, sin

radius = 5
height = 5
num_points = 4


def generate_ihlan(n=num_points, r=radius, h=height):
    """Generates an IHLAN.

    Returns:
        A list of points. First point is the top
    """
    return_points = []

    # Generate the top point
    return_points.append((0, 0, h))

    # Generate base points
    for i in range(n):
        angle = i * 2 * 3.14159265 / n
        return_points.append(
            (round(r*cos(angle), 5), round(r*sin(angle), 5), 0))

    return return_points


def export_vtk(points, filename):
    """Exports a list of points to a vtk file.

    Args:
        points: A list of points.
        filename: The filename to export to.
    """
    header = '# vtk DataFile Version 3.0\nIHLAN example\nASCII\nDATASET POLYDATA\n'

    file = open(filename, 'w')
    file.write(header)

    # Write points
    file.write(f'POINTS {len(points)} float\n')
    for point in points:
        file.write(f'{point[0]} {point[1]} {point[2]}\n')

    # Write lines
    file.write(f'LINES {2*(len(points)-1)} {2*(len(points)-1) * 3}\n')
    for i in range(1, len(points)):
        file.write(f'2 {0} {i}\n')
    for i in range(1, len(points)-1):
        file.write(f'2 {i} {i+1}\n')
    file.write(f'2 {i+1} {1}\n')

    # Write side polygons
    file.write(f'POLYGONS {len(points)} {len(points) * 4}\n')
    for i in range(1, len(points)-1):
        file.write(f'3 {0} {i} {i+1}\n')
    file.write(f'3 {0} {1} {i+1}\n')

    # Wirte the base polygon
    file.write(f'POLYGONS 1 {len(points)}\n{len(points)-1}')
    for i in range(1, len(points)):
        file.write(f' {i}')

    file.close()


if __name__ == '__main__':
    points = generate_ihlan()
    export_vtk(points, 'ihlan.vtk')
