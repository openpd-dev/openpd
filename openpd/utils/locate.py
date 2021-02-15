def findFirst(target, goal):
    for i, j in enumerate(goal):
        if j == target:
            return i
    return -1

def findFirstLambda(judgement, goal):
    for i, j in enumerate(goal):
        if judgement(j):
            return i
    return -1

def findAll(target, goal):
    res = []
    for i, j in enumerate(goal):
        if j == target:
            res.append(i)
    return res

def findAllLambda(judgement, goal):
    res = []
    for i, j in enumerate(goal):
        if judgement(j):
            res.append(i)
    return res

def binarySearch(target, goal):
    left, right = 0, len(goal) - 1
    if target >= goal[-1]:
        return right
    while left <= right:
        pivot = left + (right - left) // 2
        if goal[pivot] == target:
            return pivot
        if target < goal[pivot]:
            right = pivot - 1
        else:
            left = pivot + 1
    # As now right is smaller than left, 
    # so return right as the index for nearest smaller index
    return right
