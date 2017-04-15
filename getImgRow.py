import numpy as np
from PIL import Image


def get_num(im, position=0.5, axis=0, windows_rate=80):
    r, g, b = im.split()
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)
    t = 1 * (255-r) + 1 * (255-g) +1 * (255-b)
    pos = (t.shape[axis]-1)*position
    pos = int(pos)
    if axis == 0:
        y = np.asarray(t)[pos,:]
    else:
        y = np.asarray(t)[:,pos]
    ny = []
    windows_length = t.shape[axis]/windows_rate
    for i in range(len(y)):
        t = 0
        for j in range(windows_length):
            if i - j >= 0:
                t = t + y[i - j]
            else:
                break
        ny.append(t)
    num = 0
    nt = 1 * ny > np.max(ny)*0.05
    for i in range(len(nt)):
        if i - 1 > 0 and nt[i - 1] and not nt[i]:
            num = num + 1
    if nt[-1]:
        num = num + 1
    return num
