import csv


# from bp.bp import *


def basic():
    """
    with open("send_messages_client.txt", 'a+') as sen:
        if sen.read():
            return sen.readlines()
        else:
            return input('发送信息:')
    """
    return input('发送信息:')


def test(sg):
    if sg == 1:
        return [['1', '2.1'], ['3', '4.3'], ['5', '6.7']]
    elif sg == 2:
        return [['9.6', '8'], ['7.8', '6'], ['5.0', '4']]
    else:
        return csv_data()


def csv_data():
    with open("sd_msg_clt.csv", 'r+', encoding='utf-8', newline='') as data:
        data_read = csv.reader(data)

        msg = [row for row in data_read]
        try:
            for i in range(len(msg)):
                for j in range(len(msg[i])):
                    msg[i][j] = str(msg[i][j])
        except ValueError:
            print('数据错误')

        return msg


def bpm(k, bp1):
    # w1 = [['1', '2', '3']]
    # b1 = [['1', '1', '1']]
    # w2 = [['1'], ['2'], ['3']]
    # b2 = [['4']]
    w1, b1, w2, b2 = bp1.show_data()
    m = [w1, b1, w2, b2]
    ans = []
    for i in range(4):
        ans.append(trans_t(m[i]))
    return ans[k]


def trans_t(m):
    r = len(m)
    col = len(m[0])
    for x in range(r):
        for y in range(col):
            m[x][y] = str(m[x][y])
    return m
