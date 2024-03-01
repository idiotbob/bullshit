import csv


def input_data():
    with open("sd_msg_clt.csv", 'w+', encoding='utf-8', newline='') as sd_msg_clt:
        write = csv.writer(sd_msg_clt)

        n = int(input('输入矩阵行数:'))
        print('输入数据:')
        data = []
        for i in range(n):
            data.append(list(map(int, input().rstrip().split())))

        write.writerows(data)


def show_data():
    with open("sd_msg_clt.csv", 'r+', encoding='utf-8', newline='') as test:
        read = csv.reader(test)

        res = [row for row in read]
        try:
            for i in range(len(res)):
                for j in range(len(res[i])):
                    res[i][j] = int(res[i][j])
        except ValueError:
            print('数据错误')

        print(res)


input_data()
show_data()
