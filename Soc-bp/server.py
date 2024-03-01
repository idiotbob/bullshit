import socket
import sys
import threading
import func

import msg_src_svr
import record_server


class Server:
    def __init__(self, port):
        # 本地域名及端口
        self.host = socket.gethostname()
        self.port = 8888

        self.s = None  # 套接字
        self.sending = ''  # 发送的信息
        self.receive = ''  # 接受的信息
        self.conn = []  # 已建立的连接套接字

        self.state = []  # 套接字状态 0则删除对应套接字信息
        self.manu = []  # 已连接ip
        self.state_e = 1

        self.result = []
        self.row = 0

    def server_op(self):
        # 创建套接字并绑定端口
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建
        print(self.host, self.port)
        print('Socket created')
        try:
            self.s.bind((self.host, self.port))  # 绑定
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        print('Socket bind complete')
        self.s.listen(10)  # 开始监听
        print('Socket now listening')

    def detect(self):  # 检测连接并更新套接字表
        conn, addr = self.s.accept()
        if conn not in self.conn:
            self.conn.append(conn)
            self.manu.append(addr[0])
            self.state.append(1)
        print('与 ' + addr[0] + '连接')

    def communications(self):
        self.server_op()  # 初始化
        a = 1
        while 1:
            if a:
                while 1:
                    self.detect()  # 检测新连接
                    if input('已连接:' + str(self.manu) + '连接结束？[y|n]:') == 'y':
                        a = 0
                        break
            # print('开始传输')
            for i in range(0, len(self.conn)):  # 若存在连接，则对各连接套接字传递信息
                if self.state[i]:  # 数据传输
                    try:
                        self.conn[i].sendall('%'.encode())
                        com = threading.Thread(target=self.messages(i))
                        com.start()
                    except (ConnectionAbortedError, ConnectionResetError):
                        # self.state_e = 0
                        sys.exit()

                try:
                    self.result[-1] = trans(self.result[-1])  # 矩阵数据类型转换
                except IndexError:
                    pass

            if 1 not in self.state:  # 若全部套接字断开，返回结果，关闭服务器
                try:
                    for c in self.conn:
                        c.sendall('##'.encode())
                        self.row = int(c.recv(4096).decode())
                except (ConnectionAbortedError, ConnectionResetError):
                    self.state_e = 0
                    sys.exit()
                # print('传输结束')

                # record_server.csv_data1(self.row, self.result)  # 数据保存

                try:
                    res = func.average_m(self.result)  # 数据处理
                except IndexError:
                    res = []

                for c in self.conn:  # 结果返回
                    c.sendall(str(len(res)).encode())
                    for d in res:
                        c.sendall(str(d).encode())
                        c.recv(1024)  # 防止传输接收数据错乱

                self.dep_res()  # 矩阵分割
                self.result = []
                for i in range(len(self.state)):
                    self.state[i] = 1

            print('已连接:' + str(self.manu), end='\r')

            if self.state_e == 0:
                sys.exit()

    def send_message(self, i):
        # 向第i个套接字发送信息
        self.sending = msg_src_svr.test()  # 根据信息来源函数生成发送信息
        try:
            self.conn[i].sendall(self.sending.encode())
        except ConnectionAbortedError:
            print(str(self.manu[i]) + '连接中断')
            self.state[i] = 0

    def recv_message(self, i):
        # 从第i个套接字接收信息
        try:
            # print('等待接收:' + str(i) + ' ' + str(self.manu[i]))
            try:
                self.receive = self.conn[i].recv(4096).decode()
            except ConnectionAbortedError:
                print(str(self.manu[i]) + '连接中断')
                self.state[i] = 0
            if self.receive == '#':
                return 0
            else:
                return 1
        except (ConnectionResetError, ConnectionAbortedError):  # 无法接收则显示断开，删除该套接字
            print(str(self.manu[i]) + '连接中断')
            self.state[i] = 0

    def messages(self, i):
        # 与第i个套接字信息传递
        data = []
        while 1:

            k = self.recv_message(i)  # 如果收到'#'k为0，不再发送
            if k:
                self.send_message(i)

            if self.receive != '#':
                data.append(self.receive)

            # print(self.receive)

            try:
                if self.receive == '#':  # 收到‘#’表示信息暂时传输完毕，
                    self.conn[i].sendall('#'.encode())  # 让客户端结束信息传递进程
                    self.state[i] = 0
                    self.result.append(data)
                    break
            except (ConnectionResetError, ConnectionAbortedError):
                break

    def dep_res(self):  # 矩阵分割
        length = len(self.result[0])
        column = int(length / self.row)
        for col in self.result:
            i = self.result.index(col)
            mid = []
            while col:
                mid.append(col[:column])
                col = col[column:]
            self.result[i] = mid


def trans(x):  # 矩阵数据类型转化
    ans = []
    for d in x:
        ans.append(float(d))
    return ans
    # for m in x:
    #     x = x.index(m)
    #     for d in m:
    #         y = m.index(d)
    #         x[x][y] = float(d)
    # return x

