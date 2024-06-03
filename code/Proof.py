import math
import numpy as np


def toMeter(num):
    return num * 1852


pi = math.pi
alpha = 1.5 * pi / 180
theta = 2 * pi / 3
D_max = 110 + math.tan(alpha) * toMeter(2)
D_min = 110 - math.tan(alpha) * toMeter(2)


def question3(beta, delta_d, line_d, flag):  # line_d 是测线间距,delta_d 是船沿线距离(求一条测线用miu，两条用phi# ) flag为0向下
    yita_list = []
    a = math.sqrt(math.cos(alpha) ** 2 / (1 - math.sin(alpha) ** 2 * math.cos(beta) ** 2))  # a = cos(phi)
    b = math.sqrt(math.cos(alpha) ** 2 / (1 - math.sin(alpha) ** 2 * math.cos(beta - 0.5 * pi) ** 2))  # b = cos(miu)
    phi = math.acos(a)  # 求覆盖宽度
    miu = math.acos(b)  # 求水深
    if flag == 0:  # 从坡底开始计算
        D_shen = D_max  # 深度关于ling_d的关系
        D_qian = D_shen - line_d * math.tan(phi)
    elif flag == 2:  # 从坡顶开始计算
        D_qian = D_min  # 深度关于ling_d的关系
        D_shen = D_min + line_d * math.tan(phi)
    BE = math.sin(0.5 * theta) * D_shen / math.sin(0.5 * pi - 0.5 * theta - phi)  # 正弦定理
    AB = math.sin(0.5 * pi + phi) * D_shen / math.sin(0.5 * pi - 0.5 * theta - phi)
    AC = math.sin(0.5 * pi - 0.5 * theta - phi) * AB / math.sin(0.5 * pi - 0.5 * theta + phi)
    CE = BE * AC / AB  # 角平分线定理
    W_1 = CE + BE
    proportion = CE / W_1
    similar_ratio = D_qian / D_shen
    W_2 = W_1 * similar_ratio

    for delta_d in np.arange(0, delta_d, 10):
        if flag == 0:
            D_shen_single = D_shen - delta_d * math.tan(miu)
            D_qian_single = D_qian - delta_d * math.tan(miu)
        if flag == 2:
            D_shen_single = D_shen + delta_d * math.tan(miu)
            D_qian_single = D_qian + delta_d * math.tan(miu)
        BE = math.sin(0.5 * theta) * D_shen_single / math.sin(0.5 * pi - 0.5 * theta - phi)  # 正弦定理
        AB = math.sin(0.5 * pi + phi) * D_shen_single / math.sin(0.5 * pi - 0.5 * theta - phi)
        AC = math.sin(0.5 * pi - 0.5 * theta - phi) * AB / math.sin(0.5 * pi - 0.5 * theta + phi)
        CE = BE * AC / AB  # 角平分线定理
        W_1 = CE + BE
        proportion = CE / W_1
        similar_ratio = D_qian_single / D_shen_single
        W_2 = W_1 * similar_ratio
        yita = round((proportion * W_2 + (1 - proportion) * W_1 - line_d / math.cos(phi)) / W_2, 10)
        yita_list.append(yita)

    return (D_shen, D_qian), W_2 * math.cos(phi), yita_list, proportion, phi


def check(eta_list):
    return max(eta_list) <= 0.2 and min(eta_list) >= 0.1


def mid_line_check(beta):
    if math.tan(beta - 0.5 * pi) < 2:
        ld = ((4 - 2 / math.tan(pi - beta)) * math.sin(pi - beta)) * 1852
        delta_d = 2 * 1852 / math.cos(beta - pi / 2)
        D, W_2, yita_list, proportion, phi = question3(beta, delta_d, ld, 0)
    elif math.tan(beta - 0.5 * pi) == 2:
        print("特殊")
    elif math.tan(beta - 0.5 * pi) > 2:
        ld = ((2 - 4 * math.tan(pi - beta)) * math.cos(pi - beta)) * 1852
        delta_d = 4 * 1852 / math.cos(pi - beta)
        D, W_2, yita_list, proportion, phi = question3(beta, delta_d, ld, 2)
    return check(yita_list)


# 证伪中间的
for beta in np.arange(90.0, 180.0, 0.1):
    b = beta * pi / 180
    print('beta', beta)
    print(mid_line_check(b))
    print("-----------------------")

# 证伪斜率较大的
for beta in np.arange(150, 180, 0.1):
    beta_hudu = beta * pi / 180
    k = math.tan(beta - 90)

    right_list = []
    false_list = []

    right_list_all = []
    false_list_all = []

    for b in np.arange(0, 4 * 1852, 1):
        distance = (4 * 1852 - b) / math.cos(pi - beta_hudu)
        D, W_2, yita_list, proportion, phi = question3(beta, distance, b * math.cos(beta_hudu - pi / 2), 2)

        if check(yita_list):
            right_list.append([beta, b, max(yita_list), min(yita_list)])
        else:
            false_list.append([beta, b, max(yita_list), min(yita_list)])
    right_list_all = right_list_all + right_list
    false_list_all = false_list_all + false_list

print(right_list_all)
print(false_list_all)
