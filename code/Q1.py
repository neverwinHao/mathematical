import math
pi = math.pi
alpha = 1.5 * pi / 180
theta = 2 * pi / 3
delta_d = 200  # 相邻测线间距
D_0 = 70 - (-1000 * math.tan(alpha))  # 测线为-1000的深度，

def question1():
    D = D_0 - delta_d * math.tan(alpha)
    BE = math.sin(0.5 * theta) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)  # 正弦定理
    AB = math.sin(0.5 * pi + alpha) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)
    AC = math.sin(0.5 * pi - 0.5 * theta - alpha) * AB / math.sin(0.5 * pi - 0.5 * theta + alpha)
    CE = BE * AC / AB  # 角平分线定理
    W_1 = CE + BE
    proportion = CE / W_1
    similar_ratio = D / D_0
    W_2 = W_1 * similar_ratio
    yita = round((proportion * W_1 + (1 - proportion) * W_2 - delta_d / math.cos(alpha)) / W_2, 10)
    return D, W_2*math.cos(alpha), yita

for i in range(-800, 1000, 200):
    (depth, width, yita) = question1()
    D_0 = depth
    print("测线距中心点处的距离：", i)
    print("海水深度：", round(depth, 3))
    print("覆盖宽度：", round(width, 3))
    print("与前一条测线重叠率：", yita)
    print("--------------------------")