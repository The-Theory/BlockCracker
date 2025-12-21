import cv2 as cv
import numpy as np

def crop_to_color(img, b, g, r, x_offset=0, y_offset=0) -> np.ndarray:
    border = find_color(img, b, g, r)
    left_x = np.min(border[:, 0])
    right_x = np.max(border[:, 0])
    top_y = np.min(border[:, 1])
    bottom_y = np.max(border[:, 1])
    img = img[top_y - y_offset:bottom_y, left_x - x_offset:right_x]

    assert top_y != bottom_y
    assert left_x != right_x

    return img

def find_color(img, b, g, r):
    tol = np.array([5, 5, 5], dtype=np.uint8)  # B,G,R tolerance
    center = np.array([b, g, r], dtype=np.uint8)
    lower = np.clip(center - tol, 0, 255).astype(np.uint8)
    upper = np.clip(center + tol, 0, 255).astype(np.uint8)

    mask = cv.inRange(img, lower, upper)
    coords = cv.findNonZero(mask)

    # Color needs to be present
    assert coords is not None, "Go to settings -> Default Skin: Apply"

    return coords[:, 0]  # convert shape (N,1,2) → (N,2)

def color_at(img, color, x, y):
    for i in range(3):
        if abs(img[y, x][i] - color[i]) < 10:
            print(f"Did not find {color}, found {img[y, x]}")
            return False
    return True
