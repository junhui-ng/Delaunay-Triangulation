import cv2
import numpy as np
from typing import List

from geometric import Circle, Edge, Point, Triangle
from utils import get_supertriangle


def bowyer_watson(points: List[Point]) -> List[Triangle]:
    """
    Bowyer-Watson Algorithm
    Based on pseudocode: https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm#Pseudocode

    Arg:
        points (List[Point]) : List of points
    
    Return:
        List[Triangle] : Triangles
    """
    triangulation: List[Triangle] = []

    # compute and add supertriangle into the triangulation
    supertriangle: Triangle = get_supertriangle(points)
    triangulation.append(supertriangle)

    for point in points:
        # add all the points one at a time to the triangulation
        bad_triangles: List[Triangle] = list()
        for triangle in triangulation:
            # first find all the triangles that are no longer valid due to the insertion
            circumcenter: Circle = triangle.get_circumcircle()
            if not circumcenter or circumcenter.enclose(point):
                bad_triangles.append(triangle)

        polygon: List[Edge] = list()
        exclude_edge: List[Edge] = list()
        for triangle in bad_triangles:
            # find the boundary of the polygonal hole
            for edge in triangle.edges:
                if edge in polygon:
                    exclude_edge.append(edge)
                    polygon.remove(edge)
                if edge not in exclude_edge:
                    polygon.append(edge)
            # remove the bad triangle from the triangulation
            triangulation.remove(triangle)
        
        for edge in polygon:
            # re-triangulation the polygonal hole
            new_triangle: Triangle = Triangle(vertices=[
                edge.vertices[0], edge.vertices[1], point
            ])
            triangulation.append(new_triangle)

    result: List[Triangle] = list()
    for triangle in triangulation:
        # remove triangles that contain vertex from the supertriangle
        if not triangle.has_common_vertex(supertriangle):
            result.append(triangle)

    return result


if __name__ == "__main__":
    """
    Generate sample points
    """
    image_width: int = 500
    image_height: int = 500
    num_samples: int = 50
    image = np.zeros((image_height, image_width, 3), np.uint8)

    # randomly sample points
    points = np.random.randint(50, 450, (num_samples, 2))
    points = [Point(x=x, y=y) for (x,y) in points]
    for point in points:
        cv2.circle(image, point.xy, 1, (255, 255, 255), 2)

    # delaunay triangulation
    triangles = bowyer_watson(points)
    for triangle in triangles:
        triangle.draw(image, color=(0, 255, 0), thickness=1)
    
    cv2.imwrite("result.png", image)
