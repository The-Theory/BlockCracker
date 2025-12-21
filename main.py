import mss
import cv2 as cv
import numpy as np

from solver import solve_from_img
from placing import show_grid

region = {"top": 100, "left": 10, "width": 380, "height": 700}

with mss.mss() as sct:
    while True:
        frame = np.array(sct.grab(region))[:, :, :3]  # BGR
        frame = np.ascontiguousarray(frame, dtype=np.uint8)

        # cv.imshow("Block Blast", frame)
        # cv.moveWindow("Block Blast", 1200, 100)
        if cv.waitKey(1) & 0xFF == 27:
            break

        solution = solve_from_img(frame)

        print(f"{"-"*5} BEST* SOLUTION {"-"*5} ")
        for piece, grid in solution:
            print("Piece:")
            show_grid(piece)

            print("Result:")
            show_grid(grid)
            print("\n\n\n")
        break
