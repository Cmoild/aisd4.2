import numpy as np

lumQ = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])


chromQ = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]])

def GetQuantMatrix(quality, isLuminance = True):
    scaleFactor = 5000 / quality if quality <= 50 else 200 - quality * 2
    if isLuminance:
        lumQuantMatrix = lumQ.copy()
        for i in range(8):
            for j in range(8):
                lumQuantMatrix[i][j] = np.ceil((lumQuantMatrix[i][j] * scaleFactor + 50)/100)
        return lumQuantMatrix
    else:
        chromQuantMatrix = chromQ.copy()
        for i in range(8):
            for j in range(8):
                chromQuantMatrix[i][j] = np.ceil((chromQuantMatrix[i][j] * scaleFactor + 50)/100)
        return chromQuantMatrix
    
def Quantize(Cdct, isLuminance = True, Q = 50):
    quantMatrix = GetQuantMatrix(Q, isLuminance) if isLuminance else GetQuantMatrix(50, False)
    for i in range(8):
        for j in range(8):
            Cdct[i][j] = np.round(Cdct[i][j] / quantMatrix[i][j])
            #print(Cdct[i][j])
            #Cdct[i][j] = np.int8(Cdct[i][j])
            #print('Int ', np.int8(Cdct[i][j]))
    return np.int8(np.matrix.round(Cdct, 0))

def Dequantize(Cdct, isLuminance = True, Q = 50):
    quantMatrix = GetQuantMatrix(Q, isLuminance) if isLuminance else GetQuantMatrix(50, False)
    Cdct = np.float32(Cdct)
    for i in range(8):
        for j in range(8):
            #print(np.round(Cdct[i][j] * quantMatrix[i][j]))
            #print('int ', np.round(np.int8(Cdct[i][j]) * quantMatrix[i][j]))
            Cdct[i][j] = np.round(Cdct[i][j] * quantMatrix[i][j])
    return Cdct

