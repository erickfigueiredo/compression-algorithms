import numpy as np
from copy import deepcopy


class Quadrant:
    """
    A class to represent a quadrant (Node) in a quadtree.
    """

    def __init__(self, x: int, y: int, width: int, height: int, depth: int = 0) -> None:
        """
        Constructor for the Quadrant class.
        :param x: Origin X-coordinate of the quadrant in the quadtree.
        :param y: Origin Y-coordinate of the quadrant in the quadtree.
        :param width: Width of the quadrant in the quadtree.
        :param height: Height of the quadrant in the quadtree.
        :param depth: Depth of the quadrant in the quadtree.
        """
        self.origin = {'x': x, 'y': y}
        self.__width = width
        self.__height = height

        self.__depth = depth
        self.__children = []

    @property
    def width(self) -> int:
        """
        Getter for the width of the quadrant.
        :return: Width of the quadrant.
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        Getter for the height of the quadrant.
        :return: Height of the quadrant.
        """
        return self.__height

    @property
    def depth(self) -> int:
        """
        Getter for the depth of the quadrant.
        :return: Depth of the quadrant.
        """
        return self.__depth

    @property
    def children(self) -> list:
        """
        Getter for the children of the quadrant.
        :return: All children nodes of the quadrant.
        """
        return deepcopy(self.__children)

    @children.setter
    def children(self, children: list) -> None:
        """
        Setter for the children of the quadrant.
        :param children: List of children quadrants.
        :return: None
        """
        self.__children = children

    def get_area(self) -> int:
        """
        Method to calculate the area of the quadrant.
        :return: Area of the quadrant.
        """
        return self.__width * self.__height

    def get_quadrant_from_image(self, image: np.ndarray) -> np.ndarray:
        """
        Method to get the quadrant from the image.
        :param image: Target image to extract the quadrant from.
        :return: Quadrant of the image.
        """
        return image[self.origin['y']:self.origin['y'] + self.__height,
               self.origin['x']:self.origin['x'] + self.__width]

    def calc_error(self, image: np.ndarray) -> float:
        """
        Method to calculate the error of the quadrant.
        :param image: Target image to calculate the error from.
        :return: Error (std) of the quadrant considering the mean color.
        """
        quadrant = self.get_quadrant_from_image(image)
        mean_color = self.__calc_mean_color(quadrant)

        return np.sqrt(np.mean((quadrant - mean_color) ** 2))

    def __calc_mean_color(self, quadrant: np.ndarray) -> np.ndarray:
        """
        Method to calculate the mean color of the quadrant.
        :param quadrant: Target quadrant to calculate the mean color from.
        :return: Mean color of the quadrant.
        """
        return [int(p) for p in np.mean(quadrant, axis=(0, 1))]
