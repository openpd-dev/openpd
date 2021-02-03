def findFirst(traget, list):
    for i, j in enumerate(list):
        if j == traget:
            return i
    return -1

def findAll(traget, list):
    res = []
    for i, j in enumerate(list):
        if j == traget:
            res.append(i)
    return res