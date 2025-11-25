"""https://github.com/linbojin/Skeletonization-by-Zhang-Suen-Thinning-Algorithm/blob/master/thinning.py#L17"""
import numpy as np

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
