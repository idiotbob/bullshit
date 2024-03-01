def average(matrix):
    res = []
    row = len(matrix[0])
    column = len(matrix)
    for i in matrix:
        res.append(sum(i))
    return sum(res) / (row * column)


def average_m(matrix):
    length = len(matrix[0])
    res = [0] * length
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            res[c] += matrix[r][c]
    for i in range(length):
        res[i] /= len(matrix)
    return res
