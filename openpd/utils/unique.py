def uniqueList(list):
    res = []
    for i in list:
        if not i in res:
            res.append(i)
    return res

# Use in PDBLoader
def mergeSameNeighbor(list):
    res = [list[0]]
    for i in list:
        if i != res[-1]:
            res.append(i)
    return res