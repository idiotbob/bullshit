import client
import bp_t.bp
from bp_t.source.number import *

# x, y = source()
x, y = csv_data(10, 20)  # 分别为样本数和特征数

x = x[3:]
y = y[3:]

bp1 = bp_t.bp.BP(x, y, 1000, 0.01, 1)

client1 = client.Client('', 8888, 1)
client1.client_op()
bp1.train(client1)

# q = x[1]
# bp1.predict(q)
