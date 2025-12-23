import cv2 as cv
import numpy
import numpy as np
from mss.tools import to_png

from color_tools import *

tile_size = 18
def scan_pieces(img: np.ndarray):
    scanned_pieces = [{}, {}, {}]
    img = crop_to_color(img, 118, 60, 46, x_offset=6, y_offset=6)
    piece_img_width = img.shape[1] // 3

    # If it picks up on blue block above
    # Shrink y axis
    if img.shape[0] > tile_size * 6:
        img = img[-tile_size * 6:, :]
    # cv.imshow("Pieces", img)
    # cv.waitKey(0)

    # Get rough img estimates
    piece_imgs = [
        img[:, :piece_img_width - 10],
        img[:, piece_img_width:piece_img_width * 2],
        img[:, piece_img_width * 2 + 10:]
    ]

    # Fix each img
    for i in range(3):
        piece_imgs[i] = crop_to_color(piece_imgs[i], 119, 60, 46, x_offset=6, y_offset=6)
    #     cv.imshow(f"Piece {i + 1}", piece_imgs[i])
    # cv.waitKey(0)

    # Represent in dict
    for i, piece in enumerate(scanned_pieces):
        piece_img = piece_imgs[i]
        piece_height = piece_img.shape[0] // tile_size
        piece_width = piece_img.shape[1] // tile_size

        # Skinny patch
        if piece_width == 0:
            scanned_pieces[i] = {(0, i): True for i in range(4)}
            continue

        for x in range(piece_width):
            for y in range(piece_height):
                block_x = tile_size // 2 + x * tile_size
                block_y = tile_size // 2 + y * tile_size

                bright = max(piece_img[block_y][block_x])
                piece[x, y] = bright > 150
    return scanned_pieces
