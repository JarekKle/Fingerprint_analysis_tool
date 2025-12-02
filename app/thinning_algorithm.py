"""https://github.com/linbojin/Skeletonization-by-Zhang-Suen-Thinning-Algorithm/blob/master/thinning.py#L17"""
import numpy as np
from PIL import ImageOps
def neighbours(x, y, image):
    """Return 8-neighbours of image point P1(x,y), clockwise order."""
    img = image
    x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
    return [
        img[x_1][y],  img[x_1][y1], img[x][y1],  img[x1][y1],   # P2,P3,P4,P5
        img[x1][y],   img[x1][y_1], img[x][y_1], img[x_1][y_1]  # P6,P7,P8,P9
    ]

def transitions(neighbours):
    """Count transitions 0→1 in circular order."""
    n = neighbours + neighbours[0:1]
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

def zhangSuen(image):
    """
    Zhang-Suen thinning algorithm.
    INPUT:  PIL binarny (0/255) -> przekazany jako NumPy array
    OUTPUT: NumPy (0/1)
    """


    from PIL import ImageOps

    inverted = ImageOps.invert(image)
    img = np.array(inverted)
    img = (img > 0).astype(np.uint8)

    rows, cols = img.shape
    changing1 = changing2 = True

    while changing1 or changing2:

        # --- STEP 1 ---
        changing1 = []
        for x in range(1, rows - 1):
            for y in range(1, cols - 1):
                if img[x][y] != 1:
                    continue

                n = neighbours(x, y, img)
                P2,P3,P4,P5,P6,P7,P8,P9 = n

                if (2 <= sum(n) <= 6 and
                    transitions(n) == 1 and
                    P2 * P4 * P6 == 0 and
                    P4 * P6 * P8 == 0):
                    changing1.append((x, y))

        for x, y in changing1:
            img[x][y] = 0

        # --- STEP 2 ---
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, cols - 1):
                if img[x][y] != 1:
                    continue

                n = neighbours(x, y, img)
                P2,P3,P4,P5,P6,P7,P8,P9 = n

                if (2 <= sum(n) <= 6 and
                    transitions(n) == 1 and
                    P2 * P4 * P8 == 0 and
                    P2 * P6 * P8 == 0):
                    changing2.append((x, y))

        for x, y in changing2:
            img[x][y] = 0
    img[img == 1] = 255
    return img






DELETION_TABLE = {
    3, 6, 7, 12, 14, 15, 24, 28, 30, 31,
    48, 56, 60, 62, 63, 96, 112, 120, 124, 126,
    127, 129, 131, 135, 143, 159, 191, 192, 193,
    195, 199, 207, 223, 224, 225, 227, 231, 239,
    240, 241, 243, 247, 248, 249, 251, 252, 253,
    254
}

WEIGHTS = np.array([
    [128,   1,   2],
    [ 64,   0,   4],
    [ 32,  16,   8]
], dtype=np.uint16)


def normalize_input(image):
    """
    Akceptuje PIL.Image lub NumPy array i zwraca obraz 0/1.
    """
    # Konwersja do 0/1
    if image.max() > 1:
        image = (image > 127).astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    return image

def compute_weight(x, y, img):
    region = img[x-1:x+2, y-1:y+2]
    return int(np.sum(region * WEIGHTS))

def mark_pixels(img):
    h, w = img.shape
    for x in range(1, h-1):
        for y in range(1, w-1):
            if img[x, y] != 1:
                continue

            neigh = img[x-1:x+2, y-1:y+2].copy()
            neigh[1, 1] = 0
            count = int(neigh.sum())

            if count == 1:
                img[x, y] = 2
            elif count == 2:
                img[x, y] = 3
            elif count in (3, 4):
                img[x, y] = 4


def kmm(image):
    """
    KMM thinning algorithm.
    INPUT:  PIL.Image (binary 0/255)
    OUTPUT: NumPy array (0/255)
    """
    inverted = ImageOps.invert(image)
    img = np.array(inverted)

    img = (img > 0).astype(np.uint8)

    rows, cols = img.shape
    changed = True

    neigh = [(-1,0), (-1,1), (0,1), (1,1),
             (1,0), (1,-1), (0,-1), (-1,-1)]

    while changed:
        changed = False
        pixels_to_remove = []

        for x in range(1, rows-1):
            for y in range(1, cols-1):
                if img[x, y] != 1:
                    continue

                # Pobierz 8-sąsiadów
                n = [img[x+dx, y+dy] for dx,dy in neigh]

                # KMM – warunki
                S = sum(n)
                T = sum((n[i] == 0 and n[(i+1)%8] == 1) for i in range(8))

                if not (2 <= S <= 6):
                    continue
                if T != 1:
                    continue
                if n[0] * n[2] * n[4] != 0:
                    continue
                if n[2] * n[4] * n[6] != 0:
                    continue

                pixels_to_remove.append((x, y))

        if pixels_to_remove:
            changed = True
            for x, y in pixels_to_remove:
                img[x,y] = 0

    img[img == 1] = 255
    return img