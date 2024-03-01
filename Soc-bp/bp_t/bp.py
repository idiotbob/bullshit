import random
import csv
import sys
import time

sys.path.insert(0, 'bp_t')
from matrix_cul.matrix_c import *
from function import func, d_func
from data_src import import_data, import_data2


class BP:
    def __init__(self, x, y, max_c, alpha, f_set):
        self.x = x  # 样本输入
        self.y = y  # 样本输出
        self.max_c = max_c  # 循环次数
        self.alpha = alpha  # 学习率
        self.f_set = f_set  # 激活函数设置

        self.s_in = len(x[0])  # feature
        self.s_out = len(y[0])  # 输出结果大小
        self.sample = len(x)  # 样本数

        self.n_hind = 2 * self.s_in + 1  # 隐藏层大小

        self.w1 = []  # 权重矩阵
        self.w2 = []
        self.b1 = []  # 偏置矩阵
        self.b2 = []

        self.hind_o = []  # 隐藏层输出
        self.ans = []  # 结果输出

        self.ex_state = 0
        # self.waiting = 1
        self.control = 1

    def train(self, client1):
        self.init_matrix()  # 初始化权重、偏置矩阵
        cyc = 0
        while cyc < self.max_c:
            self.trans_f()  # 正向传播

            d2, d1 = self.delta()  # 反向传播，偏差计算

            self.renew(d2, d1)  # 更新权重、偏置矩阵

            cyc += 1

            if cyc % 100 == 0:  # 展示进度
                print('{}%'.format(100 * cyc / self.max_c))

            if cyc % 10 == 0:
                self.ex_state = 1
                # self.waiting = 1
                client1.communicate(self)
                self.ex_state = 0

        self.control = 0
        self.record()  # 权重、偏置矩阵记录
        print('训练结果:')
        print(trans_t(self.ans, 3))
        print('样本结果:')
        print(self.y)
        print('偏差:')
        print(self.error())

    def predict(self, x):
        self.read_data()
        hind_in = io_meth_single(x, self.w1, self.b1,
                                 self.n_hind, self.s_in,
                                 1, self.f_set)
        ans = io_meth_single(hind_in, self.w2, self.b2,
                             self.s_out, self.n_hind,
                             1, self.f_set)
        print('ans:')
        print(trans(ans, 0))

    def init_matrix(self):
        self.w1 = random_matrix(self.n_hind, self.s_in)
        self.w2 = random_matrix(self.s_out, self.n_hind)
        self.b1 = random_matrix(1, self.n_hind)
        self.b2 = random_matrix(1, self.s_out)

    def error(self):
        E = []
        for k in range(self.sample):
            e = 0
            for i in range(self.s_out):
                e += 0.5 * (self.ans[k][i] - self.y[k][i]) ** 2
            E.append(e)
        return E

    def trans_f(self):
        self.hind_o = io_meth(self.x,
                              self.w1, self.b1,
                              self.n_hind, self.s_in, len(self.x),
                              1, self.f_set)
        self.ans = io_meth(self.hind_o,
                           self.w2, self.b1,
                           self.s_out, self.n_hind, len(self.hind_o),
                           1, self.f_set)

    def delta(self):
        d2 = self.delta2()
        d1 = self.delta1(d2)
        return d2, d1

    def renew(self, d2, d1):
        self.w2 = plus_m(self.w2, times_m(-self.alpha, mul(tm(d2), self.hind_o)))
        self.w2 = r_one(self.w2)
        self.b2 = plus_m(self.b2, [times(-self.alpha, average(d2))])

        self.w1 = plus_m(self.w1, times_m(-self.alpha, mul(tm(d1), self.x)))
        self.w1 = r_one(self.w1)
        self.b1 = plus_m(self.b1, [times(-self.alpha, average(d1))])

    def show_data(self):
        return self.w1, self.b1, self.w2, self.b2

    def upgrade(self, w1, b1, w2, b2):
        self.w1 = w1
        self.b1 = b1
        self.w2 = w2
        self.b2 = b2

    def read_data(self):
        m_f = import_data()
        self.w1 = m_f[0]
        self.b1 = m_f[1]
        self.w2 = m_f[2]
        self.b2 = m_f[3]
        d_f = import_data2()
        self.f_set = d_f[0][0]
        self.s_in = d_f[0][1]
        self.s_out = d_f[0][2]

    def delta2(self):
        mid = []
        d = io_meth(self.hind_o,
                    self.w2, self.b1,
                    self.s_out, self.n_hind, len(self.hind_o),
                    0, self.f_set)
        for i in range(self.sample):
            m = multiply(d[i], plus(self.ans[i], times_m(-1, self.y)[i]))
            mid.append(m)
        return mid

    def delta1(self, delta):

        ans = []
        d = io_meth(self.x,
                    self.w1, self.b1,
                    self.n_hind, self.s_in, len(self.x),
                    0, self.f_set)

        for n in range(self.sample):
            mid = [0] * len(d[0])
            for k in range(self.s_out):
                m = times(delta[n][k], self.w2[k])
                mid = plus(mid, m)
            ans.append(multiply(mid, d[n]))
        return ans

    def record(self):
        m = [self.w1, self.b1, self.w2, self.b2]
        n = ['w1', 'b1', 'w2', 'b2']
        for i in range(4):
            with open('{}record.csv'.format(n[i]),
                      'w+',
                      encoding='utf-8',
                      newline='') as cs:
                write = csv.writer(cs)

                write.writerows(m[i])
        bd = [self.f_set, self.s_in, self.s_out]
        with open('basic_data.csv',
                  'w+',
                  encoding='utf-8',
                  newline='') as cs:
            write = csv.writer(cs)
            write.writerow(bd)


def io_meth(indata, w, b, n_later, n_former, n_sample, s, f_set):
    odata = []
    for n in range(n_sample):
        zn = []
        for j in range(n_later):
            zj = 0
            for i in range(n_former):
                zj += w[j][i] * indata[n][i]
            zj -= b[0][j]
            if s:
                zj = func(zj, f_set)
            else:
                zj = d_func(zj, f_set)
            zn.append(zj)
        odata.append(zn)
    return odata


def io_meth_single(feature, w, b, n_later, n_former, s, f_set):
    zn = []
    for j in range(n_later):
        zj = 0
        for i in range(n_former):
            zj += w[j][i] * feature[i]
        zj -= b[0][j]
        if s:
            zj = func(zj, f_set)
        else:
            zj = d_func(zj, f_set)
        zn.append(zj)
    return zn


def random_matrix(row, col):
    w = []
    for s2 in range(row):
        wk = []
        for s1 in range(col):
            wk.append(random.random())
        s = sum(wk)
        for i in range(col):
            wk[i] /= s
        w.append(wk)
    return w
