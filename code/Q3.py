import math
import numpy as np

pi = math.pi
alpha = 1.5 * pi / 180
theta = 2 * pi / 3
D_max = 110 + math.tan(alpha) * 2*1852
D_0 = D_max - 358.625 * math.tan(alpha)
line_list = []
yita_list = []
def parallel(line_d):
    global D_0
    D = D_0 - line_d * math.tan(alpha)
    BE = math.sin(0.5 * theta) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)  # 正弦定理
    AB = math.sin(0.5 * pi + alpha) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)
    AC = math.sin(0.5 * pi - 0.5 * theta - alpha) * AB / math.sin(0.5 * pi - 0.5 * theta + alpha)
    CE = BE * AC / AB  # 角平分线定理
    W_1 = CE + BE
    proportion = CE / W_1
    similar_ratio = D / D_0
    W_2 = W_1 * similar_ratio
    yita = round((proportion * W_1 + (1 - proportion) * W_2 - line_d / math.cos(alpha)) / W_2, 10)
    return D, W_2*math.cos(alpha), yita
sum_line_d =0
for line_d in np.arange(650,0,-0.01):
    D, W_2, yita = parallel(line_d)
    if yita>0.1 and yita<0.1005:
        D_0 = D
        if sum_line_d > 4*1852-358.625:
            break
        elif 4*1852 - sum_line_d - 358.625 < 22.527:
            break
        else:
            line_list.append(line_d)
            sum_line_d += line_d
print(line_list)
print(len(line_list)+1)
print(sum_line_d)
