import cv2 as cv
import numpy
import numpy as np

from util import *

def scan_pieces(img: np.ndarray):
    scanned_pieces = []
    img = crop_to_color(img, 119, 60, 51, x_offset=13, y_offset=14)
    piece_img_width = img.shape[1] // 3

    piece_imgs = [
        img[:, :piece_img_width],
        img[:, piece_img_width:piece_img_width * 2],
        img[:, piece_img_width * 2:]
    ]

    for i in range(3):
        piece_imgs[i] = crop_to_color(piece_imgs[i], 119, 60, 51, x_offset=13, y_offset=14)
        piece_imgs[i] = piece_imgs[i][:-7, :-7]

        cv.imshow(f"Piece {i+1}", piece_imgs[i])

    cv.waitKey(0)
    return scanned_pieces
