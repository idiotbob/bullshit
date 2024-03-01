import csv


def import_data():
    ans = []
    n = ['w1', 'b1', 'w2', 'b2']
    for i in range(4):
        with open('{}record.csv'.format(n[i]),
                  'r+',
                  encoding='utf-8',
                  newline='') as cs:
            read = csv.reader(cs)

            res = [row for row in read]
            try:
                for i in range(len(res)):
                    for j in range(len(res[i])):
                        res[i][j] = float(res[i][j])
            except ValueError:
                print('数据错误')

            ans.append(res)
    return ans


def import_data2():
    ans = []
    with open('basic_data.csv',
              'r+',
              encoding='utf-8',
              newline='') as cs:
        read = csv.reader(cs)

        res = [row for row in read]
        try:
            for i in range(len(res)):
                for j in range(len(res[i])):
                    res[i][j] = int(res[i][j])
        except ValueError:
            print('数据错误')
    return res
