import csv


c0 = [[0, 1, 0],
      [1, 0, 1],
      [1, 0, 1],
      [1, 0, 1],
      [0, 1, 0]]

c1 = [[0, 1, 0],
      [1, 1, 0],
      [0, 1, 0],
      [0, 1, 0],
      [1, 1, 1]]

c2 = [[0, 1, 0],
      [1, 0, 1],
      [0, 0, 1],
      [0, 1, 0],
      [1, 1, 1]]

c3 = [[1, 1, 0],
      [0, 0, 1],
      [0, 1, 0],
      [0, 0, 1],
      [1, 1, 0]]

c4 = [[0, 0, 1],
      [0, 1, 1],
      [1, 0, 1],
      [1, 1, 1],
      [0, 0, 1]]

c5 = [[1, 1, 1],
      [1, 0, 0],
      [1, 1, 0],
      [0, 0, 1],
      [1, 1, 0]]

c6 = [[0, 1, 1],
      [1, 0, 0],
      [1, 1, 0],
      [1, 0, 1],
      [0, 1, 0]]

c7 = [[1, 1, 1],
      [0, 0, 1],
      [0, 1, 0],
      [1, 0, 0],
      [1, 0, 0]]

c8 = [[0, 1, 0],
      [1, 0, 1],
      [1, 1, 1],
      [1, 0, 1],
      [0, 1, 0]]

c9 = [[0, 1, 0],
      [1, 0, 1],
      [0, 1, 1],
      [0, 0, 1],
      [1, 1, 0]]

char = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]


def num_c():
    num = []
    for n in char:
        mid = []
        for row in n:
            mid += row
        num.append(mid)
    return num


def tar():
    targ = []
    for i in range(10):
        t = [0] * 10
        t[i] = 1
        targ.append(t)
    return targ


def source():
    return num_c(), tar()


def csv_data(num=100, fea=-2):
    with open("train.csv", 'r+', encoding='utf-8', newline='') as data:
        data_read = csv.reader(data)

        msg = []
        res = []
        i = 0
        n = 0  # 控制样本数量
        for row in data_read:
            if i:
                msg.append(row[1:fea])  # 从第二列到倒数第二列  [1:20]即为前20个特征
                res.append(row[-1])  # 标签
                n += 1
            i = 1
            if n == num:
                break
        for x in range(len(msg)):
            for y in range(len(msg[x])):
                msg[x][y] = float(msg[x][y])
        label = []
        for n in res:
            num = [0] * 10
            num[int(n)] = 1
            label.append(num)

    return msg, label
