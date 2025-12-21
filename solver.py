from itertools import permutations
from numpy import ndarray

from color_tools import *
from placing import *
from piece_finder import scan_pieces

def solve_from_img(img: ndarray):
    # Image
    pieces_img = img.copy()

    # Search for grid border
    #72, 40, 34
    border = find_color(img, 72, 38, 33)
    left_x = np.min(border[:, 0])
    right_x = np.max(border[:, 0])
    top_y = np.min(border[:, 1])
    bottom_y = np.max(border[:, 1])
    img = img[top_y:bottom_y, left_x:right_x]

    assert top_y != bottom_y
    assert left_x != right_x

    # Construct digital representation
    grid = {}
    block_pos = []
    block_size = img.shape[0] // 8
    for y in range(8):
        for x in range(8):
            grid[x, y] = False

            block_x = block_size // 2 + x * block_size
            block_y = block_size // 2 + y * block_size

            # Shoddy solution checking greatest rgb val, works though
            bright = max(img[block_y][block_x])
            if bright > 100:
                block_pos.append((block_x, block_y))
                grid[x, y] = True

    # Get pieces
    scanned_pieces = scan_pieces(pieces_img)
    print("Scanned pieces:")
    for piece in scanned_pieces:
        show_grid(piece)
        print()

    # Test every piece placement
    solutions = []
    for turn in permutations(scanned_pieces):
        piece1, piece2, piece3 = turn

        for grid1 in get_overlays(grid, piece1):
            for grid2 in get_overlays(grid1, piece2):
                for grid3 in get_overlays(grid2, piece3):
                    solutions.append(((piece1, grid1),
                                      (piece2, grid2),
                                      (piece3, grid3)))

    # Get best solution
    # Based on blocks cleared
    best_sol_index = 0
    best_sol_score = 0
    for i, sol in enumerate(solutions):
        sol_grid = sol[2][1]
        sol_score = 0
        for x in range(8):
            for y in range(8):
                if grid[x, y] and not sol_grid[x, y]:
                    sol_score += 1
        if sol_score > best_sol_score:
            best_sol_index = i
            best_sol_score = sol_score
    solution = solutions[best_sol_index]

    return solution