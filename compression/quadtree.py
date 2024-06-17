import os
import cv2
import numpy as np
from copy import deepcopy

from compression.quadrant import Quadrant


class QuadTree:
    """
    QuadTree class implementation for Image Compression.
    """

    def __init__(self, image: np.ndarray, threshold: int = None, min_quad_size: int = 1) -> None:
        """
        Constructor for the QuadTree class.
        :param image: Image to be compressed.
        :param threshold: Threshold value for quadrant split.
        :param min_quad_size: Minimum size of the quadrant.
        """
        self.__image = deepcopy(image)

        self.__threshold = threshold
        self.__min_quad_size = min_quad_size

        self.root = Quadrant(0, 0, image.shape[1], image.shape[0], 0)
        self.__build_tree(self.root)

    @property
    def max_depth(self) -> int:
        """
        Getter for the maximum depth of the quadtree.
        """
        return self.__get_max_depth(self.root)

    def get_children(self) -> list[Quadrant]:
        """
        Getter for the leaves of the quadtree.
        """
        return self.__get_children(self.root)

    def get_compressed_image(self, show_quadrants: bool = False, highlight_color: tuple = (0, 255, 0)) -> np.ndarray:
        """
        Method to get the compressed image from the quadtree.
        :param show_quadrants: Flag to show the quadrants highlighted in the compressed image.
        :param highlight_color: Color to highlight the quadrants.
        """
        compressed_image = np.zeros_like(self.__image)
        children = self.get_children()

        for child in children:
            quadrant = child.get_quadrant_from_image(self.__image)
            compressed_image[child.origin['y']:child.origin['y'] + child.height,
            child.origin['x']:child.origin['x'] + child.width, :] = child.calc_mean_color(quadrant)

        if show_quadrants:
            for child in children:
                imgc = cv2.rectangle(compressed_image, (child.origin['x'], child.origin['y']),
                                     (child.origin['x'] + child.width, child.origin['y'] + child.height),
                                     highlight_color, 1)

        return compressed_image

    def build_compressed_file(self, save_path: str = None, filename: str = None) -> None:
        """
        Method to build a compressed file from the quadtree. creates a file with ".lima" extension which contains the
        instructions for the compressed file construction.
        :param save_path: Path to save the compressed file.
        :param filename: Name of the compressed file.
        """
        if not (save_path and filename):
            raise ValueError('Please provide a save path and filename!')

        quadrants = self.get_children()
        compressed_data = '&'.join([str(quad) for quad in quadrants])

        with open(os.path.join(save_path, f'{filename}.lima'), 'w') as file:
            file.write(f'{self.__image.shape[0]};{self.__image.shape[1]}&{compressed_data}')

    @staticmethod
    def parse_compressed_file(file_path: str) -> np.ndarray:
        """
        Static Method to parse the compressed file and build the quadtree.
        :param file_path: Path to the compressed file.
        :return: Parsed image.
        """
        if not file_path.endswith('.lima'):
            raise ValueError('Invalid file extension!')

        with open(file_path, 'r') as file:
            data = file.read().split('&')

        shape = data[0].split(';')
        parsed_image = np.zeros((int(shape[0]), int(shape[1]), 3), dtype=np.uint8)

        for quad_data in data[1:]:
            quad = quad_data.split(';')
            color = [int(c) for c in quad[-1].split(',')]
            parsed_image[int(quad[1]):int(quad[3]), int(quad[0]):int(quad[2]), :] = color

        return parsed_image

    def __get_max_depth(self, quadrant: Quadrant) -> int:
        """
        Method to get the maximum depth of the quadtree recursively.
        :param quadrant: Quadrant to get the depth from.
        """
        if not quadrant.children:
            return quadrant.depth

        max_depth = 0
        for child in quadrant.children:
            max_depth = max(max_depth, self.__get_max_depth(child))

        return max_depth

    def __get_children(self, quadrant: Quadrant) -> list[Quadrant]:
        """
        Method to get the leaves of the quadtree recursively.
        :param quadrant: Quadrant to get the leaves from.
        """
        if not quadrant.children:
            return [quadrant]

        leaves = []
        for child in quadrant.children:
            leaves.extend(self.__get_children(child))

        return leaves

    def __build_tree(self, quadrant: Quadrant) -> None:
        """
        Method to build the quadtree recursively.
        :param quadrant: Quadrant to be split.
        """

        if self.__threshold and quadrant.calc_error(self.__image) <= self.__threshold:
            return

        bottom_width, top_width = np.floor(quadrant.width / 2).astype(int), np.ceil(quadrant.width / 2).astype(int)
        bottom_height, top_height = np.floor(quadrant.height / 2).astype(int), np.ceil(quadrant.height / 2).astype(int)

        if bottom_width < 1 or bottom_height < 1:
            return

        if self.__min_quad_size and (bottom_width <= self.__min_quad_size or bottom_height <= self.__min_quad_size):
            return

        top_left = Quadrant(quadrant.origin['x'], quadrant.origin['y'], bottom_width, bottom_height, quadrant.depth + 1)
        self.__build_tree(top_left)

        top_right = Quadrant(quadrant.origin['x'] + bottom_width, quadrant.origin['y'], top_width, bottom_height,
                             quadrant.depth + 1)
        self.__build_tree(top_right)

        bottom_left = Quadrant(quadrant.origin['x'], quadrant.origin['y'] + bottom_height, bottom_width, top_height,
                               quadrant.depth + 1)
        self.__build_tree(bottom_left)

        bottom_right = Quadrant(quadrant.origin['x'] + bottom_width, quadrant.origin['y'] + bottom_height, top_width,
                                top_height, quadrant.depth + 1)
        self.__build_tree(bottom_right)

        quadrant.children = [top_left, top_right, bottom_left, bottom_right]