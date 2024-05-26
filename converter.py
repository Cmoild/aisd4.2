from PIL import Image
import numpy as np

toycbcr = np.array([[0.299, 0.587, 0.114], [-0.168736, -0.331264, 0.5], [0.5, -0.418688, -0.081312]])

# преобразование изображения в YCbCr
def ToYCbCr(img):
    #img = np.array(Image.open("capybara.jpg"))
    #print(img)

    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = np.matmul(toycbcr, img[i][j]) + np.array([0, 128, 128])

    return np.uint8(img)

#print(img)
#Image.fromarray(np.uint8(img), mode="YCbCr").show()



'''
for i in range(len(img)):
    for j in range(len(img[0])):
        y, cb, cr = img[i][j]
        img[i][j][0] = y + 1.402 * (cr - 128)
        img[i][j][1] = y - 0.344136 * (cb - 128) - 0.714136 * (cr - 128)
        img[i][j][2] = y + 1.772 * (cb - 128)

#print(img)
Image.fromarray(np.uint8(img)).show()

'''