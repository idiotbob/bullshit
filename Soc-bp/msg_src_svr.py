import csv

'''
def basic():
    with open("send_messages_server.txt", 'a+') as sen:
        if sen.read():
            return sen.readlines()
        else:
            return input('发送信息:')
'''


def test():
    return '已接收'


def csv_data():
    with open("sd_msg_svr.csv", 'r+', encoding='utf-8', newline='') as data:
        data_read = csv.reader(data)

        msg = [row for row in data_read]
        try:
            for i in range(len(msg)):
                for j in range(len(msg[i])):
                    msg[i][j] = int(msg[i][j])
        except ValueError:
            print('数据错误')

        return msg
