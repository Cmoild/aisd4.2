import converter
from PIL import Image
import numpy as np
import resampling
import dct
import quantization
import zigzag

# создание матриц 8х8 из исходной
def SplitToBlocks(array, nrows=8, ncols=8):
    array = np.array(array)
    r, h = array.shape
    ret = []
    for i in range(0, r, nrows):
        subarray = np.array(array[i:i+nrows])
        #print(subarray)
        subarray = np.hsplit(subarray, h//ncols)
        #print(np.array(subarray))
        ret += subarray[::1]
    return np.array(ret)

# объединение матриц 8х8
def MergeBlocks(array, nrows, ncols):
    array = np.array(array)
    #print(array)
    h, r, c = array.shape
    ret = []
    for i in range(nrows//r):
        subarray = tuple(array[i*(ncols//r):(i+1)*(ncols//r)])
        #print(subarray)
        ret.append(np.concatenate(subarray, axis=1))
        #print(ret)
    ret = np.concatenate(ret, axis=0)
    return ret

# получение массивов сжатого изображения
def GetResultArrays(__path, qual):
    img = converter.ToYCbCr(np.array(Image.open(__path)))
    i, j, k = img.shape
    if i % 16 != 0:
        img = np.pad(img, ((0, 16 - i % 16), (0, 0), (0, 0)), 'constant')
    if j % 16 != 0:
        img = np.pad(img, ((0, 0), (0, 16 - j % 16), (0, 0)), 'constant')
    img2 = np.uint8(resampling.DownsamplingByAverage(img))
    Yc = np.int16(img[:, :, 0]) - 128
    Cb = np.int16(img2[:, :, 1]) - 128
    Cr = np.int16(img2[:, :, 2]) - 128
    #Image.fromarray(Yc).show()
    Yc = SplitToBlocks(Yc)
    Cb = SplitToBlocks(Cb)
    Cr = SplitToBlocks(Cr)

    resYc = []
    resCb = []
    resCr = []
    
    for i in range(len(Yc)):
        Yc[i] = dct.DCT(Yc[i])
        Yc[i] = quantization.Quantize(Yc[i], Q=qual)
        resYc.append(zigzag.zigzag(Yc[i]))
    for i in range(len(Cb)):
        Cb[i] = dct.DCT(Cb[i])
        Cb[i] = quantization.Quantize(Cb[i], False, Q=qual)
        resCb.append(zigzag.zigzag(Cb[i]))
    for i in range(len(Cr)):
        Cr[i] = dct.DCT(Cr[i])
        Cr[i] = quantization.Quantize(Cr[i], False, Q=qual)
        resCr.append(zigzag.zigzag(Cr[i]))
    #print(len(img2), len(img2[0]))
    return resYc, resCb, resCr, len(img2), len(img2[0])

# вывод изображения из полученных массивов
def ShowImageFromResultArrays(resYc, resCb, resCr, horiz, vert, qual):
    Yc = [None for i in range(len(resYc))]
    Cb = [None for i in range(len(resCb))]
    Cr = [None for i in range(len(resCr))]
    #print(resYc[0])
    #print(zigzag.inverseZigZag(resYc[0], 8))
    for i in range(len(Yc)):
        Yc[i] = zigzag.inverseZigZag(resYc[i], 8)
        Yc[i] = np.int16(Yc[i])
        Yc[i] = quantization.Dequantize(Yc[i], Q=qual)
        Yc[i] = dct.IDCT(Yc[i])
        #Yc.append(a)
    for i in range(len(Cb)):
        Cb[i] = zigzag.inverseZigZag(resCb[i], 8)
        Cb[i] = np.int16(Cb[i])
        Cb[i] = quantization.Dequantize(Cb[i], False, Q=qual)
        Cb[i] = dct.IDCT(Cb[i])
        #Cb.append(a)
    for i in range(len(Cr)):
        Cr[i] = zigzag.inverseZigZag(resCr[i], 8)
        Cr[i] = np.int16(Cr[i])
        Cr[i] = quantization.Dequantize(Cr[i], False, Q=qual)
        Cr[i] = dct.IDCT(Cr[i])
        #Cr.append(a)
    
    Yc = np.array(Yc)
    Cb = np.array(Cb)
    Cr = np.array(Cr)
    

    Yc = MergeBlocks(Yc, vert, horiz)
    Cb = MergeBlocks(Cb, vert//2, horiz//2)
    Cr = MergeBlocks(Cr, vert//2, horiz//2)

    img3 = np.zeros((len(Cb), len(Cb[0]), 3), dtype=np.uint8)
    img3[:, :, 1] = Cb
    img3[:, :, 2] = Cr
    img3 = resampling.UpsamplingByRepeat(img3)
    img3[:, :, 0] = Yc

    img3 = np.array(img3) + 128
    #img2 = np.concatenate((Yc, Cb, Cr), axis=3)

    img = Image.fromarray(img3, mode="YCbCr")
    img.show()
    #img.save(f"output{qual}.jpg")

# кодирование и декодирование RLE
def run_length_encoding(string):
    encoded_string = ''
    count = 1
    flag = chr(256)
    strlen = len(string)
    for i in range(1, strlen):
        if (i % 50000 == 0): print(i)
        if string[i] == string[i-1]:
            count += 1
        else:
            if count < 4:
                encoded_string += count * string[i-1]
            else:
                encoded_string += flag + chr(count) + string[i-1]
            count = 1
    if count < 4:
        encoded_string += count * string[len(string)-1]
    else:
        encoded_string += flag + chr(count) + string[len(string)-1]

    return encoded_string

def run_length_decoding(string):
    decoded_string = ''
    flag = chr(256)
    i = 0
    strlen = len(string)
    for i in range(strlen):
        if (i % 50000 == 0): print(i)
        if i >= 1 and (string[i-1] == flag or string[i-2] == flag):
            continue
        if string[i] == flag:
            decoded_string += (ord(string[i+1])) * string[i+2]
            #i += 2
        else:
            decoded_string += string[i]
            #i += 1
    return decoded_string

# сжатие изображения и запись его в файл
def Compress(__path, qual):
    resYc, resCb, resCr, img2v, img2h = GetResultArrays(__path, qual)
    #print(resYc)
    #print(len(resYc), len(resYc[0]))
    print(len(resYc), len(resCb), len(resCr))
    eY = []
    for i in resYc:
        eY += [j+128 for j in i]
    eY = ''.join([chr(i) for i in eY])
    eY = run_length_encoding(eY)

    eCb = []
    for i in resCb:
        eCb += [j+128 for j in i]
    eCb = ''.join([chr(i) for i in eCb])
    eCb = run_length_encoding(eCb)

    eCr = []
    for i in resCr:
        eCr += [j+128 for j in i]
    eCr = ''.join([chr(i) for i in eCr])
    eCr = run_length_encoding(eCr)
    print(len(eY), len(eCb), len(eCr))
    leny = len(eY).to_bytes(4, byteorder='big')
    lencb = len(eCb).to_bytes(4, byteorder='big')
    lencr = len(eCr).to_bytes(4, byteorder='big')
    quality = qual.to_bytes(1, byteorder='big')
    hor = img2h.to_bytes(2, byteorder='big')
    vert = img2v.to_bytes(2, byteorder='big')
    data = eY + eCb + eCr
    data = data.encode('utf-8')
    data = leny + lencb + lencr + quality + hor + vert + data

    with open('compressed.bin', 'wb') as f:
        f.write(data)
        f.close()

# распаковка изображения
def Show(__path):
    with open(__path, 'rb') as f:
        data = f.read()
        f.close()
    
    leny = int.from_bytes(data[0:4], byteorder='big')
    lencb = int.from_bytes(data[4:8], byteorder='big')
    lencr = int.from_bytes(data[8:12], byteorder='big')
    qual = int.from_bytes(data[12:13], byteorder='big')
    hor = int.from_bytes(data[13:15], byteorder='big')
    vert = int.from_bytes(data[15:17], byteorder='big')
    data = data[17:].decode('utf-8')
    eY = data[0:leny]
    eCb = data[leny:leny+lencb]
    eCr = data[leny+lencb:leny+lencb+lencr]
    print(leny, lencb, lencr)
    img2v, img2h = vert, hor

    resYc = []
    resCb = []
    resCr = []
    eY = run_length_decoding(eY)
    eCb = run_length_decoding(eCb)
    eCr = run_length_decoding(eCr)
    for i in eY:
        resYc += [ord(i) - 128]
    for i in eCb:
        resCb += [ord(i) - 128]
    for i in eCr:
        resCr += [ord(i) - 128]
    print(len(resYc), len(resCb), len(resCr))
    if len(resYc) % 64 != 0:
        resYc += [0] * (64 - len(resYc) % 64)
    resYc = [resYc[i:i+64] for i in range(0, len(resYc), 64)]
    resCb = [resCb[i:i+64] for i in range(0, len(resCb), 64)]
    resCr = [resCr[i:i+64] for i in range(0, len(resCr), 64)]
    ShowImageFromResultArrays(resYc, resCb, resCr, img2h*2, img2v*2, qual)

Compress("capybara.jpg", 99)
Show("compressed.bin")


