import math
import  numpy as np
pi = math.pi
alpha = 1.5 * pi / 180
theta = 2 * pi / 3
D_0 = 120

def question2(beta,delta_d):
    beta = beta * pi / 180
    a = math.sqrt(math.cos(alpha)**2/(1-math.sin(alpha)**2 * math.cos(beta)**2)) #a = cos(phi)
    b = math.sqrt(math.cos(alpha) ** 2 / (1 - math.sin(alpha) ** 2 * math.cos(beta - 0.5 * pi) ** 2))#b = cos(miu)
    phi = math.acos(a) #求覆盖宽度
    miu = math.acos(b) #求水深
    if beta < 0.5*pi or beta >1.5*pi:
        D = D_0 + delta_d * math.tan(miu)# 测线变化率
    else:
        D = D_0 - delta_d * math.tan(miu)# 测线变化率
    BE = math.sin(0.5 * theta) * D / math.sin(0.5 * pi - 0.5 * theta - phi)  # 正弦定理
    AB = math.sin(0.5 * pi + phi) * D / math.sin(0.5 * pi - 0.5 * theta - phi)
    AC = math.sin(0.5 * pi - 0.5 * theta - phi) * AB / math.sin(0.5 * pi - 0.5 * theta + phi)
    CE = BE * AC / AB  # 角平分线定理
    W_1 = CE + BE
    return D, W_1* math.cos(phi)

for beta in range(0,360,45):
    for i in np.arange(0, 2.1*1852+1, 0.3*1852):
        (depth, width) = question2(beta,i)
        # D_0 = depth
        print("当前测线角度", beta)
        print("测线距中心点处的距离：", round(i/1852/0.3,2))
        print("海水深度：", round(depth, 3))
        print("覆盖宽度：", round(width, 3))
        print("--------------------------")
