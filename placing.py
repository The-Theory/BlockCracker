# Prints representation of grid
def show_grid(grid:dict):
    width = 0
    height = 0

    for x, y in grid.keys():
        width = max(x + 1, width)
        height = max(y + 1, height)

    for y in range(height):
        row = ""
        for x in range(width):
            if grid[x, y]: row += "⏹ "
            else: row += "• "
        print(row)

# Checks if a piece can be overlayed at position
def can_overlay(bg: dict, mask: dict, x_offset: int = 0, y_offset: int = 0) -> bool:
    for x, y in mask.keys():
        new_x = x + x_offset
        new_y = y + y_offset
        if bg[new_x, new_y] and mask[x, y]: return False

    return True

# Add adds a piece to a grid
def overlay(bg: dict, mask: dict, offset) -> dict:
    result = bg.copy()
    for x, y in mask.keys():
        if not mask[x, y]: continue
        new_x = x + offset[0]
        new_y = y + offset[1]

        assert result[new_x, new_y] is False
        result[new_x, new_y] = True
    return result


# Clears full rows and cols
def process_grid(bg: dict) -> dict:
    result = {}
    rows = []
    cols = []

    # Find full rows
    for row in range(0, 8):
        is_row_full = True
        for col in range(0, 8):
            if not bg[col, row]:
                is_row_full = False
                break
        if is_row_full:
            rows.append(row)

    # Find full cols
    for col in range(0, 8):
        is_col_full = True
        for row in range(0, 8):
            if not bg[col, row]:
                is_col_full = False
                break
        if is_col_full:
            cols.append(col)

    # Copy original, except those to be cleared
    for x in range(0, 8):
        for y in range(0, 8):
            if x in cols or y in rows:
                result[x, y] = False
            else:
                result[x, y] = bg[x, y]
    return result


# Gets all possible grids as a result of placing a piece in every position possible
def get_overlays(bg: dict, piece: dict) -> list[dict]:
    overlays = []
    piece_width = 0
    piece_height = 0

    for x, y in piece.keys():
        piece_width = max(x + 1, piece_width)
        piece_height = max(y + 1, piece_height)

    for x in range(8 - piece_width + 1):
        for y in range(8 - piece_height + 1):
            if not can_overlay(bg, piece, x, y): continue
            overlays.append(process_grid(overlay(bg, piece, (x, y))))
    return overlays
