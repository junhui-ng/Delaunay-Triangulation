import cv2
import math
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Point:
    x: int
    y: int

    def distanceFrom(self, point) -> float:
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    @property
    def xy(self) -> Tuple[int, int]:
        """
        xy-coordinates of the point.

        Return: 
            Tuple[int, int] : xy-coordinates.
        """
        return (int(self.x), int(self.y))
    
    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x
    
    def draw(self, 
             image: np.ndarray, 
             color: Tuple[int] = (255,255,255),
             thickness: int = 2) -> None:
        """
        Draw the point on the image (in-place).

        Args:
            image (np.ndarray) : Image
            color (Tuple[int]) : Line color
            thickness (int) : Line thickness
        """
        cv2.circle(image, center=self.xy, radius=2, color=color, thickness=thickness)

@dataclass
class Edge:
    vertices: List[Point]

    def __post_init__(self):
        assert len(self.vertices) == 2, f"An edge has 2 vertices, {len(self.vertices)} found."
        self.vertices.sort()

    def draw(self, 
             image: np.ndarray, 
             color: Tuple[int] = (255,255,255),
             thickness: int = 2) -> None:
        """
        Draw the edge on the image (in-place).

        Args:
            image (np.ndarray) : Image
            color (Tuple[int]) : Line color
            thickness (int) : Line thickness
        """
        vertex_a, vertex_b = self.vertices
        cv2.line(image, vertex_a.xy, vertex_b.xy, color=color, thickness=thickness)

@dataclass
class Circle:
    centroid: Point
    radius: float

    def enclose(self, point: Point) -> bool:
        """
        Check if a point falls within the circle.

        Arg:
            point (Point) : Point

        Return:
            bool : True if the point falls within the circle.
        """
        return self.centroid.distanceFrom(point) <= self.radius

    def draw(self, 
             image: np.ndarray, 
             color: Tuple[int] = (255,255,255),
             thickness: int = 2) -> None:
        """
        Draw the circle on the image (in-place).

        Args:
            image (np.ndarray) : Image
            color (Tuple[int]) : Line color
            thickness (int) : Line thickness
        """
        cv2.circle(image, center=self.centroid.xy, radius=int(self.radius), color=color, thickness=thickness)


@dataclass
class Triangle:
    vertices: List[Point]

    def __post_init__(self):
        assert len(self.vertices) == 3, f"Triangle must have 3 vertices, {len(self.vertices)} found."
        self.vertices.sort()

    @property
    def edges(self) -> List[Edge]:
        """
        Edges of the triangle.

        Return:
            List[Edge] : List of edges.
        """
        return [
            Edge(vertices=[self.vertices[idx1], self.vertices[idx2]]) 
            for (idx1, idx2) in ((0,1), (1,2), (0,2))
        ]

    def get_circumcircle(self) -> Circle:
        """
        Return the circumcircle that passes through all the vertices of the triangle.

        Return:
            Circle: Circumcircle.
        """
        p1, p2, p3 = self.vertices

        det = 2 * (
            p1.x * (p2.y - p3.y) + 
            p2.x * (p3.y - p1.y) +
            p3.x * (p1.y - p2.y)
        )

        if abs(det) < 1e-10:
            # points are collinear; circumcircle is undefined
            return None

        x_c = (((p1.x * p1.x + p1.y * p1.y) * (p2.y - p3.y) +
                (p2.x * p2.x + p2.y * p2.y) * (p3.y - p1.y) +
                (p3.x * p3.x + p3.y * p3.y) * (p1.y - p2.y)) / det)

        y_c = (((p1.x * p1.x + p1.y * p1.y) * (p3.x - p2.x) +
                (p2.x * p2.x + p2.y * p2.y) * (p1.x - p3.x) +
                (p3.x * p3.x + p3.y * p3.y) * (p2.x - p1.x)) / det)

        radius = math.sqrt(
            (x_c - p1.x) * (x_c - p1.x) + 
            (y_c - p1.y) * (y_c - p1.y)
        )

        return Circle(centroid=Point(x_c, y_c), radius=radius)

    def has_common_vertex(self, other) -> bool:
        """
        Check if two triangles have common vertex.
        
        Arg:
            other (Triangle) : Triangle

        Return:
            bool: True if the two triangles have at least one common vertex.
        """
        for vertex in other.vertices:
            if vertex in self.vertices:
                return True
        return False
    
    def draw(self, 
             image: np.ndarray, 
             color: Tuple[int] = (255,255,255),
             thickness: int = 2) -> None:
        """
        Draw the triangle on the image (in-place).

        Args:
            image (np.ndarray) : Image
            color (Tuple[int]) : Line color
            thickness (int) : Line thickness
        """
        for edge in self.edges:
            vertex_a, vertex_b = edge.vertices
            cv2.line(image, vertex_a.xy, vertex_b.xy, color=color, thickness=thickness)
