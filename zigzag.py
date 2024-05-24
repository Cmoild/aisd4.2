import numpy as np


def zigzag(a):
    res = []
    x, y = 0, 0
    for i in range(len(a)*2-1):
        run = []
        while x in range(len(a)) and y in range(len(a)):
            run.append(a[y][x])
            x -= 1
            y += 1
        if i < len(a)-1:
            x = i + 1
            y = 0
        else:
            x = len(a)-1
            y = (i + 1) % len(a) + 1
        if i % 2 == 0:
            run = run[::-1]
        res += run

    return res

def inverseZigZag(res, n):
    b = np.zeros((n, n))
    x, y = 0, 0
    h = 0
    numsInRun = 0
    for i in range(n*2-1):
        if i < n:
            numsInRun += 1
        else:
            numsInRun -= 1
        run = [x for x in res[h:h+numsInRun]]
        if i % 2 != 0:
            run = run[::-1]
        numN = 0
        #print(run)
        while x in range(n) and y in range(n):
            #run.append(a[y][x])
            b[x][y] = run[numN]
            numN += 1
            h += 1
            x -= 1
            y += 1
        if i < n-1:
            x = i + 1
            y = 0
        else:
            x = n-1
            y = (i + 1) % n + 1

    return b

'''
a = np.random.randint(0, 100, (8, 8))
res = zigzag(a)

print(res)
b = inverseZigZag(res, 8)

print(np.int8(b) == a)
'''