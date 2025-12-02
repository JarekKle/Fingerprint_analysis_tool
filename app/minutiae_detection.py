"""https://github.com/linbojin/Skeletonization-by-Zhang-Suen-Thinning-Algorithm/blob/master/thinning.py#L17"""
import numpy as np
import cv2
def neighbours(x, y, image):
    """Return 8-neighbours of image point P1(x,y), clockwise order."""
    P = [
        image[x+1][y],     # S
        image[x+1][y+1],   # SE
        image[x][y+1],     # E
        image[x-1][y+1],   # NE
        image[x-1][y],     # N
        image[x-1][y-1],   # NW
        image[x][y-1],     # W
        image[x+1][y-1]    # SW
    ]
    # zwracamy 0/1 jako int, nie uint8
    return [1 if p > 0 else 0 for p in P]

def calculate_cn_value(P):
    cn = 0
    for i in range(8):
        cn += 0.5 * abs(P[i] - P[(i+1) % 8])
    return cn

def remove_close_minutiae(minutiae, min_distance=10):
    minutiae = minutiae.copy()
    result = []

    # sortujemy tak, aby najpierw były te z większym typem
    minutiae.sort(key=lambda m: m[2], reverse=True)

    removed = set()

    for i, m1 in enumerate(minutiae):
        if i in removed:
            continue

        x1, y1, t1 = m1
        keep = True

        for j, m2 in enumerate(minutiae):
            if i == j or j in removed:
                continue

            x2, y2, t2 = m2
            dist = np.hypot(x1 - x2, y1 - y2)

            if dist < min_distance:
                # m1 ma większy typ, bo wcześniej sortowaliśmy
                removed.add(j)

        result.append(m1)

    return result
def remove_border_minutiae(minutiae, border_thresh=5,diagonal=0.15, auto_thresh=False):
    if len(minutiae) == 0:
        return []

    # konwersja na numpy dla wygody
    pts = np.array(minutiae)
    xs = pts[:, 0]
    ys = pts[:, 1]

    minX, maxX = np.min(xs), np.max(xs)
    minY, maxY = np.min(ys), np.max(ys)
    wid, hei = maxX-minX, maxY-minY
    border_thresh = max(wid,hei)*0.08
    leftX, rightX = minX+diagonal*wid, maxX-diagonal*wid
    leftY, rightY = minY+diagonal*hei, maxY-diagonal*hei

    borders = [
        (leftX, leftY),
        (leftX, rightY),
        (rightX, leftY),
        (rightX, rightY)
    ]
    filtered = []
    for (x, y, type) in minutiae:
        remove = False

        # ---- 1. Zbyt blisko krawędzi obrazu ----
        if (
            abs(x - minX) < border_thresh or
            abs(x - maxX) < border_thresh or
            abs(y - minY) < border_thresh or
            abs(y - maxY) < border_thresh
        ):
            remove = True

        # ---- 2. Zbyt blisko przekątnych (czterech rogów wewnątrz) ----
        if not remove:  # tylko jeśli jeszcze nie usunięty
            for (bx, by) in borders:
                if abs(x - bx) < border_thresh and abs(y - by) < border_thresh:
                    remove = True
                    break

        # Zachowujemy tylko jeśli NIE był oznaczony do usunięcia
        if not remove:
            filtered.append([x, y, type])

    return filtered
def crossingnumber(image, remove_border = True, remove_close = True, border_thresh=35):
    minutiae = []
    img = np.array(image)
    rows, cols = img.shape

    out = img.copy()  # żeby nie nadpisywać w miejscu
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):

            if img[x][y] != 255:
                continue

            P = neighbours(x, y, img)
            cn = calculate_cn_value(P)

            # if cn == 0:
            #     out[x][y] = 40
            #     minutiae.append([x,y,cn])
            # elif cn == 1:
            #     out[x][y] = 80
            #     minutiae.append([x,y,cn])
            # elif cn == 3:
            #     out[x][y] = 160
            #     minutiae.append([x,y,cn])
            # elif cn == 4:
            #     out[x][y] = 200
            #     minutiae.append([x,y,cn])
            if cn in (0,1,3,4):
                minutiae.append([x, y, cn])
    if remove_close:
        minutiae = remove_close_minutiae(minutiae)
    if remove_border:
        minutiae = remove_border_minutiae(minutiae, border_thresh=border_thresh, auto_thresh=True)
    return out, minutiae