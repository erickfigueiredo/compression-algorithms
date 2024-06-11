import os
import cv2
import numpy as np
from copy import deepcopy

from compression.quadrant import Quadrant


class QuadTree:
    def __init__(self, image: np.ndarray, threshold: int = None, min_quad_size: int = 1) -> None:
        self.__image = deepcopy(image)

        self.__threshold = threshold
        self.__min_quad_size = min_quad_size

        self.root = Quadrant(0, 0, image.shape[1], image.shape[0], 0)
        self.__build_tree(self.root)

    @property
    def max_depth(self) -> int:
        return self.__get_max_depth(self.root)

    def get_leaves(self) -> list[Quadrant]:
        return self.__get_leaves(self.root)

    def get_compressed_image(self, show_quadrants: bool = False, highlight_color: tuple = (0, 255, 0)) -> np.ndarray:
        compressed_image = np.zeros_like(self.__image)
        children = self.get_leaves()

        for child in children:
            quadrant = child.get_quadrant_from_image(self.__image)
            compressed_image[child.origin['y']:child.origin['y'] + child.height,
            child.origin['x']:child.origin['x'] + child.width, :] = child.calc_mean_color(quadrant)

        if show_quadrants:
            for child in children:
                imgc = cv2.rectangle(compressed_image, (child.origin['y'], child.origin['x']),
                                     (child.origin['y'] + child.height, child.origin['x'] + child.width),
                                     highlight_color, 1)

        return compressed_image

    def build_compressed_file(self, save_path:str=None, filename:str=None) -> None:
        if not (save_path and filename):
            raise ValueError('Please provide a save path and filename!')

        quadrants = self.get_leaves()
        compressed_data = '&'.join([str(quad) for quad in quadrants])

        with open(os.path.join(save_path, f'{filename}.lima'), 'wb') as file:
            file.write(str.encode(compressed_data))


    def __get_max_depth(self, quadrant: Quadrant) -> int:
        if not quadrant.children:
            return quadrant.depth

        max_depth = 0
        for child in quadrant.children:
            max_depth = max(max_depth, self.__get_max_depth(child))

        return max_depth

    def __get_leaves(self, quadrant: Quadrant) -> list[Quadrant]:
        if not quadrant.children:
            return [quadrant]

        leaves = []
        for child in quadrant.children:
            leaves.extend(self.__get_leaves(child))

        return leaves

    def __build_tree(self, quadrant: Quadrant) -> None:

        if self.__threshold and quadrant.calc_error(self.__image) <= self.__threshold:
            return

        bottom_width, top_width = np.floor(quadrant.width / 2).astype(int), np.ceil(quadrant.width / 2).astype(int)
        bottom_height, top_height = np.floor(quadrant.height / 2).astype(int), np.ceil(quadrant.height / 2).astype(int)

        if self.__min_quad_size and bottom_width <= self.__min_quad_size and bottom_height <= self.__min_quad_size:
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
