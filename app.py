import cv2
from compression.quadtree import QuadTree


if __name__ == '__main__':
    img = cv2.imread('./images/example_1.png')
    img_compressed = QuadTree(image=img, threshold=30, min_quad_size=10)
    img_compressed.build_compressed_file(save_path='./', filename='example_1')
