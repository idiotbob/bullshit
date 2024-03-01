def times(n, x):  # 向量数乘
    ans = []
    for xd in x:
        ans.append(n * xd)
    return ans


def times_m(n, x):  # 矩阵数乘
    ans = []
    for xx in range(len(x)):
        ans.append(times(n, x[xx]))
    return ans


def multiply(x, y):  # 向量内积
    ans = []
    for i in range(len(x)):
        ans.append(x[i] * y[i])
    return ans


def multiply_m(x, y):  # 向量外积
    ans = []
    for i in range(len(x)):
        ans.append(times(x[i], y))
    return ans


def tm(x):
    ans = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    return ans


def plus(x, y):  # 向量加法
    ans = []
    for i in range(len(x)):
        ans.append(x[i] + y[i])
    return ans


def plus_m(x, y):  # 矩阵加法
    ans = []
    for i in range(len(x)):
        ans.append(plus(x[i], y[i]))
    return ans


def ml(x, y):
    ans = 0
    length = len(x)
    for i in range(length):
        ans += x[i] * y[i]
    return ans


def mul(x, y):
    ans = []
    y1 = tm(y)
    for i in range(len(x)):
        col = []
        for j in range(len(y1)):
            col.append(ml(x[i], y1[j]))
        ans.append(col)
    return ans


def ad(x):
    ans = [0] * len(x[0])
    for i in x:
        ans = plus(i, ans)
    return ans


def average(x):
    ans = ad(x)
    ans = times(1.0 / len(x), ans)
    return ans


def trans_t(x, n):
    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j] = round(x[i][j], n)
    return x


def trans(x, n):
    for i in range(len(x)):
        x[i] = round(x[i], n)
    return x


def r_one(x):
    ans = []
    for i in x:
        ans.append(times(1.0 / sum(i), i))
    return ans
