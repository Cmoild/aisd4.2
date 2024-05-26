import numpy as np

# Даунсемплинг удалением
def DownsamplingByDelete(img):
    return img[::2, ::2, :]

# Апсемплинг повторением
def UpsamplingByRepeat(img):
    return np.repeat(np.repeat(img, 2, axis=0), 2, axis=1)

from PIL import Image

# Даунсемплинг взятием среднего значения
def DownsamplingByAverage(img):
    i, j, k = img.shape
    sh = [i, j, k]
    if sh[0] % 2 != 0:
        sh[0] -= 1
    if sh[1] % 2 != 0:
        sh[1] -= 1
    newimg = np.zeros([sh[0]//2, sh[1]//2, 3], dtype=np.uint8)
    for i in range(0, sh[0], 2):
        for j in range(0, sh[1], 2):
            for k in range(0, sh[2]):
                newimg[i//2, j//2, k] = (img[i, j, k]/4 + img[i+1, j, k]/4 + img[i, j+1, k]/4 + img[i+1, j+1, k]/4)
    return newimg

# Даунсемплинг взятием ближайшего к среднему значению
def DownsamplingByNearToAverage(img):
    i, j, k = img.shape
    sh = [i, j, k]
    if sh[0] % 2 != 0:
        sh[0] -= 1
    if sh[1] % 2 != 0:
        sh[1] -= 1
    newimg = np.zeros([sh[0]//2, sh[1]//2, 3], dtype=np.uint8)
    for i in range(0, sh[0], 2):
        for j in range(0, sh[1], 2):
            for k in range(0, sh[2]):
                newimg[i//2, j//2, k] = (img[i, j, k]/4 + img[i+1, j, k]/4 + img[i, j+1, k]/4 + img[i+1, j+1, k]/4)
                m = 256
                for l in range(2):
                    for h in range(2):
                        a = np.int16(newimg[i//2, j//2, k]) - img[i+l, j+h, k]
                        if abs(a) < m:
                            m = a
                        newimg[i//2, j//2, k] = img[i+l, j+h, k]
                
    return newimg

#Image.fromarray(UpsamplingByRepeat(DownsamplingByNearToAverage(np.array(Image.open("capybara.jpg"))))).show()