def process_piece(piece_str:str):
    piece = {}
    x = y = 0

    for line in piece_str:
        for char in line:
            if char == "\n": continue
            piece[x, y] = char == "#"
            x += 1
        x = 0
        y += 1
    return len(piece_str[0]), len(piece_str), piece


def can_overlay(bg: dict, mask: dict, x_offset: int = 0, y_offset: int = 0) -> bool:
    for x, y in mask.keys():
        new_x = x + x_offset
        new_y = y + y_offset
        if bg[new_x, new_y] and mask[x, y]: return False

    return True


def overlay(bg: dict, mask: dict, offset) -> dict:
    result = bg.copy()
    for x, y in mask.keys():
        if not mask[x, y]: continue
        new_x = x + offset[0]
        new_y = y + offset[1]

        assert result[new_x, new_y] is False
        result[new_x, new_y] = True
    return result


def get_overlays(bg: dict, piece: str):
    overlays = []

    width, height, mask = process_piece(piece)
    for x in range(8 - width + 1):
        for y in range(8 - height + 1):
            if not can_overlay(bg, mask, x, y): continue
            overlays.append(process_grid(overlay(bg, mask, (x, y))))
    return overlays


def process_grid(bg: dict) -> dict:
    result = {}
    rows = []
    cols = []

    for row in range(0, 8):
        is_row_full = True
        for col in range(0, 8):
            if not bg[col, row]:
                is_row_full = False
                break
        if is_row_full:
            rows.append(row)
    for col in range(0, 8):
        is_col_full = True
        for row in range(0, 8):
            if not bg[col, row]:
                is_col_full = False
                break
        if is_col_full:
            cols.append(col)

    for x in range(0, 8):
        for y in range(0, 8):
            if x in cols or y in rows:
                result[x, y] = False
            else:
                result[x, y] = bg[x, y]
    return result
