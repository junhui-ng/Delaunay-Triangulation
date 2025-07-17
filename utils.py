from typing import List

from geometric import Point, Triangle


def get_supertriangle(points: List[Point]) -> Triangle:
    """
    Given a set of points, return the supertriangle that encloses all points.

    Arg:
        points (List[Point]) : List of points
    
    Return:
        Triangle : Supertriangle.
    """
    # get the bounding rectangle that encloses all points
    x: int = max(0, min([pt.x for pt in points]) - 5)
    y: int = max(0, min([pt.y for pt in points]) - 5)
    w: int = max([pt.x for pt in points]) + 5 - x
    h: int = max([pt.y for pt in points]) + 5 - y

    # supertriangle
    triangle = Triangle(vertices=[
        Point(x=x, y=y),
        Point(x=x, y=y+2*h),
        Point(x=x+2*w, y=y)
    ])

    return triangle