import socket
import sys
# from bp.bp import *
import threading
import time

import msg_src_clt
import record_client


class Client:
    def __init__(self, tar_host, tar_port, test):
        # 连接
        self.s = None
        # 域名ip端口
        self.tar_host = tar_host
        self.tar_ip = ''
        self.tar_port = tar_port
        # 信息
        self.sending = ''
        self.receive = ''
        # 接收状态 1表示可进行信息传递
        self.sr_state = 1
        # 套接字状态 0则退出程序
        self.state = 1
        # 矩阵行数
        self.row = 0
        # 控制输入数据来源
        self.test = test
        # 返回数据长度
        self.reply_len = 0

    def client_op(self):
        # 建立套接字连接
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('创建失败')
            sys.exit()

        print('连接已创建')

        try:
            self.tar_ip = socket.gethostbyname(self.tar_host)
        except socket.gaierror:
            print('域名解析失败')
            sys.exit()

        try:
            self.s.connect((self.tar_ip, self.tar_port))
        except socket.error:
            print('连接失败')
            sys.exit()

        print('已连接 ' + self.tar_host + ' ip: ' + self.tar_ip)

    def communicate(self, bp1):
        ex_state = 1
        if ex_state:
            reply_m = []
            for k in range(4):  # 分别传输4个矩阵
                self.row = 0
                while 1:  # 矩阵传输
                    self.receive = self.s.recv(4096).decode()
                    if self.receive == '%':  # 接收到'%'后开始信息传递
                        self.sr_state = 1
                        while 1:
                            if self.sr_state:

                                for data_list in msg_src_clt.bpm(k, bp1):  # 传递矩阵数据
                                    for data in data_list:
                                        self.sending = data.encode()
                                        self.s.sendall(self.sending)
                                        self.recv_message()
                                    self.row += 1  # 记录矩阵行数

                                self.sending = '#'.encode()  # 结束该传递过程
                                self.s.sendall(self.sending)
                                self.recv_message()  # 接收返回控制信息

                            else:
                                break
                    elif self.receive == '##':  # ##时断开连接
                        self.state = 0

                    if self.state == 0:
                        self.sending = str(self.row).encode()  # 返回行数
                        self.s.sendall(self.sending)

                        self.recv_message()
                        self.reply_len = self.receive  # 接收数据长度

                        reply = []
                        for i in range(int(self.reply_len)):
                            reply.append(float(self.s.recv(4096).decode()))
                            self.s.sendall(' '.encode())  # 防止接收错乱

                        ans = dep_res(reply, self.row)  # 将接收列表转换为矩阵
                        # print('reply:')
                        # print(ans)
                        reply_m.append(ans)  # [w1,b1,w2,b2]

                        break
                self.state = 1
            bp1.upgrade(reply_m[0], reply_m[1], reply_m[2], reply_m[3])

    def send_message(self):
        #  '#'结束，’%‘开始
        self.sending = msg_src_clt.basic().encode()
        self.s.sendall(self.sending)

    def recv_message(self):
        self.receive = self.s.recv(4096).decode()
        # print(self.receive)  # test
        if self.receive == '#':
            self.sr_state = 0
        # if self.receive == '##':  # 收到##时关闭客户端
        #     self.state = 0  # test
        # record_client.basic(self.receive.decode())


def dep_res(matrix, row):  # 分割矩阵
    length = len(matrix)
    column = int(length / row)

    mid = []
    while matrix:
        mid.append(matrix[:column])
        matrix = matrix[column:]
    return mid
