import cv2 as cv
import numpy
import numpy as np

from color_tools import *

tile_size = 55
def scan_pieces(img: np.ndarray):
    scanned_pieces = [{}, {}, {}]
    img = crop_to_color(img, 119, 60, 51, x_offset=13, y_offset=14)
    piece_img_width = img.shape[1] // 3

    # Get rough img estimates
    piece_imgs = [
        img[:, :piece_img_width],
        img[:, piece_img_width:piece_img_width * 2],
        img[:, piece_img_width * 2:]
    ]

    # Fix each img
    for i in range(3):
        piece_imgs[i] = crop_to_color(piece_imgs[i], 119, 60, 51, x_offset=13, y_offset=14)
        piece_imgs[i] = piece_imgs[i][:-7, :-7]

    # Represent in dict
    for i, piece in enumerate(scanned_pieces):
        piece_img = piece_imgs[i]
        piece_height = piece_img.shape[0] // tile_size
        piece_width = piece_img.shape[1] // tile_size

        for x in range(piece_width):
            for y in range(piece_height):
                block_x = tile_size // 2 + x * tile_size
                block_y = tile_size // 2 + y * tile_size

                bright = max(piece_img[block_y][block_x])
                piece[x, y] = bright > 150

    return scanned_pieces
