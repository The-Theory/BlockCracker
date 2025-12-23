import math
import time

import mss
import cv2 as cv
import numpy as np
import pyautogui as gui

from solver import solve_from_img
from placing import show_grid, Placement

region = {"top": 100, "left": 10, "width": 390, "height": 700}

def print_solution(solution: list[Placement]):
    print(f"{"-" * 5} BEST* SOLUTION {"-" * 5} ")
    for place in solution:
        print(f"Piece at ({place.x}, {place.y}):")
        show_grid(place.piece)

        print("Result:")
        show_grid(place.grid)
        print("\n\n\n")

def go_to_board(x: int, y: int):
    block_size = region["width"] / 8.5
    target_x = region["left"] + 35 + x * block_size
    target_y = region["top"] + 190 + y * block_size

    mouse_x, mouse_y = gui.position()

    rel_x = target_x - mouse_x
    rel_y = target_y - mouse_y

    # rel_x /= 1.1
    # rel_y /= 2

    rel_x = (rel_x + 47) / 1.3
    rel_y = (rel_y + 147)/1.30093

    gui.dragRel(rel_x, rel_y, 0, button='left')

piece_offset = 50
piece_buffer = region["width"] * 0.15
piece_area_width = region["width"] - piece_buffer * 2
piece_y = region["height"] + piece_offset
piece_positions = (
    (piece_buffer + piece_offset/2, piece_y),
    (region["width"]/2, piece_y),
    (region["width"] - piece_buffer - piece_offset/2, piece_y)
)

# gui.moveTo(piece_positions[2])
# go_to_board(0, 0)
# quit()

with mss.mss() as sct:
    while True:
        if cv.waitKey(1) & 0xFF == 27: break
        frame = np.array(sct.grab(region))[:, :, :3]  # BGR
        frame = np.ascontiguousarray(frame, dtype=np.uint8)

        pieces_matrix = []
        sol = solve_from_img(frame, pieces_matrix)
        print_solution(sol)
        move_order = [place.piece_id for place in sol]

        gui.moveTo(region["width"]/2, region["height"]/2)
        gui.click()

        for moveid, piece_index in enumerate(move_order):
            move = sol[moveid]

            # Drag piece
            gui.moveTo(piece_positions[piece_index])
            go_to_board(move.x, move.y)

        gui.moveTo(0, 0, duration=1)