import bp
from source.number import source

# x = [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0]]
# y = [[1, 0], [0, 1], [1, 1]]

x, y = source()  # 极简像素画识别

q = x[0]  # 预测目标（可以自己改）

bp1 = bp.BP(x, y, 1000, 0.01, 1)

# 可单独运行train()或predict()函数（取消或添加注释即可）
# bp1.train()  # 训练模型，并把训练得到的权重、偏置矩阵记录为csv文件
bp1.predict(q)  # 预测，读取csv文件中数据，并用于计算q的输出
