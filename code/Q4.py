import numpy as np
import math

#定义常用常量
pi = math.pi

# 得到的坡面的方向向量
line_1 = np.array([1663.46,1699.62,-15.64])
line_2 = np.array([1602.43,-541.29,-53.38])

# print(line_1[0])

# 得到平面的法相向量
plane_1=np.array([0.0046,0.0047,1])
plane_2=np.array([0.0299,-0.0101,1])

# 计算叉乘,即测线的方向向量
cexian_1 = np.cross(line_1, plane_1)
cexian_2 = np.cross(line_2, plane_2)

# print(cexian_1)
# print(cexian_2)

#计算beta
pingmian = np.array([0,0,1])

touying_mian_1 = np.cross(pingmian,plane_1)
touying_mian_2 = np.cross(pingmian,plane_2)

po_faxian_touying_1 = np.cross(touying_mian_1,plane_1)
po_faxian_touying_2 = np.cross(touying_mian_2,plane_2)

cerxian_mo_1 = np.sqrt(cexian_1.dot(cexian_1))
cerxian_mo_2 = np.sqrt(cexian_2.dot(cexian_2))

po_faxian_touying_mo_1 = np.sqrt(po_faxian_touying_1.dot(po_faxian_touying_1))
po_faxian_touying_mo_2 = np.sqrt(po_faxian_touying_2.dot(po_faxian_touying_2))

#四舍五入
beta_1 = (np.arccos(cexian_1.dot(po_faxian_touying_1)/(float(cerxian_mo_1*po_faxian_touying_mo_1)))*180/np.pi)
beta_2 = (np.arccos(cexian_2.dot(po_faxian_touying_2)/(float(cerxian_mo_2*po_faxian_touying_mo_2)))*180/np.pi)

# print(beta_1)
# print(beta_2) 

#定义所需常量
#坡度
alpha_1 = 0.377
alpha_2 = 1.808

#定义张角范围
theta = [i for i in np.arange(2*pi/3,5*pi/6,pi/50)]

#定义海水深度，此时的海水深度我们认为是随着拟合坡面的深度
D_1_min = 13.640
D_2_max = 223.932

line_list_1 = []
line_list_2 = []

def parallel_1(line_d, alpha, D_0, theta):
    D = D_0 + line_d * math.tan(alpha)
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



def parallel_2(line_d, alpha, D_0, theta):
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

# print(parallel(595))

#先求出最大平移距离 
#该直线为(x-3.8*1852)/(line_2[0])=(y-4*1852)/line_2[1]与
#(x-3.8*1852)/(line_2[0])=(z+82.5931)line_2[2]
#则存在一特殊点(3.8*1852,4*1852,-82.5931)
#又有顶点坐标为(5*1852,0,-223.932)
#我们需要再找一特殊点,令x=0
special_x1_2 = 0
special_y1_2 = -3.8*1852*line_2[1]/line_2[0]+4*1852
special_z1_2 = -3.8*1852*line_2[2]/line_2[0]-82.5931

special_x2_2 = 3.8*1852
special_y2_2 = 4*1852
special_z2_2 = -82.5931

special_x3_2 = 5*1852
special_y3_2 = 0
special_z3_2 = -223.932

#利用点到直线距离公式求得平移最远点距离
point_fangxiang_1 = np.array([special_x1_2-special_x3_2,special_y1_2-special_y3_2,special_z1_2-special_z3_2])
point_fangxiang_2 = np.array([special_x2_2-special_x3_2,special_y2_2-special_y3_2,special_z2_2-special_z3_2])

chacheng_dis = np.cross(point_fangxiang_1,point_fangxiang_2)
chacheng_dis = np.sqrt(chacheng_dis.dot(chacheng_dis))

dead_d_2 = abs(chacheng_dis/np.sqrt((special_x1_2-special_x2_2)**2+(special_y1_2-special_y2_2)**2+(special_z1_2-special_z2_2)**2))
# print(dead_d)

sum_line_d_2 = 0
theta_list_2 = []

for test_theta in theta:
    for line_d in np.arange(800,300,-0.01):
        D, W_2, yita = parallel_2(line_d,alpha_2*pi/180,D_2_max,test_theta)
        if abs(yita - 0.2) < 0.05:
            D_0 = D
            if sum_line_d_2 > dead_d_2:
                break
            else:
                line_list_2.append(line_d)
                theta_list_2.append(test_theta)
                sum_line_d_2 += line_d


print(line_list_2)
print(len(line_list_2))
print(sum_line_d_2)
print(theta_list_2)



#先求出最大平移距离 
#该直线为(x-3.8*1852)/(line_1[0])=(y-4*1852)/line_1[1]与
#(x-3.8*1852)/(line_1[0])=(z+82.5931)line_1[2]
#则存在一特殊点(3.8*1852,4*1852,-82.5931)
#又有顶点坐标为(0,0,-13.6401)
#我们需要再找一特殊点,令x=0
special_x1_1 = 0
special_y1_1 = -3.8*1852*line_1[1]/line_1[0]+4*1852
special_z1_1 = -3.8*1852*line_1[2]/line_1[0]-82.5931

special_x2_1 = 3.8*1852
special_y2_1 = 4*1852
special_z2_1 = -82.5931

special_x3_1 = 0
special_y3_1 = 0
special_z3_1 = -13.6401

#利用点到直线距离公式求得平移最远点距离
point_fangxiang_1 = np.array([special_x1_1-special_x3_1,special_y1_1-special_y3_1,special_z1_1-special_z3_1])
point_fangxiang_2 = np.array([special_x2_1-special_x3_1,special_y2_1-special_y3_1,special_z2_1-special_z3_1])

chacheng_dis = np.cross(point_fangxiang_1,point_fangxiang_2)
chacheng_dis = np.sqrt(chacheng_dis.dot(chacheng_dis))

dead_d_1 = abs(chacheng_dis/np.sqrt((special_x1_2-special_x2_2)**2+(special_y1_2-special_y2_2)**2+(special_z1_2-special_z2_2)**2))
print(dead_d_1)

sum_line_d_1 = 0
theta_list_1=[]

for test_theta in theta:
    for line_d in np.arange(100,0,-0.01):
        D, W_2, yita = parallel_1(line_d,alpha_1*pi/180,D_1_min,test_theta)
        if abs(yita - 0.2) < 0.05:
            D_0 = D
            if sum_line_d_1 > dead_d_1:
                break
            else:
                line_list_1.append(line_d)
                sum_line_d_1 += line_d
                theta_list_1.append(theta)

print(line_list_1)
print(len(line_list_1))
print(sum_line_d_1)

#计算测线的总长度
sum_distance=0
for i in line_list_1:
    distance_1 = i /math.cos(beta_1-pi/2)/math.sin(beta_1-pi/2)
    sum_distance+=distance_1
for j in line_list_2:
    distance_2 = j /math.sin(beta_2-pi/2)/math.cos(beta_2-pi/2)
    sum_distance+=distance_2
print(sum_distance)

#计算漏测海区占总待测海域面积的百分比
area_all_1 = (3.8+1.4)*4/2/math.cos(beta_1)
area_all_2 = (3.8+1.4)*4/2/math.cos(beta_2)
area_all = area_all_1 +area_all_2
area_no_test_1=0
area_no_test_2=0
for i in line_list_1:
    no_test_1 = i*i/math.tan(beta_1-pi/2)/2
    area_no_test_1 += no_test_1
for j in line_list_2:
    no_test_2 = i*i*math.tan(beta_1-pi/2)/2
    area_no_test_2 += no_test_2
print((area_no_test_1+area_no_test_2)/area_all)

#计算重叠率超过20％的长度
#平行分布保证两个平面的重叠率没有超过百分之二十，只需要计算内部转折处
def parallel_ok(line_d, alpha, D_0, theta):
    D = D_0 - line_d * math.tan(alpha)
    BE = math.sin(0.5 * theta) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)  # 正弦定理
    AB = math.sin(0.5 * pi + alpha) * D_0 / math.sin(0.5 * pi - 0.5 * theta - alpha)
    AC = math.sin(0.5 * pi - 0.5 * theta - alpha) * AB / math.sin(0.5 * pi - 0.5 * theta + alpha)
    CE = BE * AC / AB  # 角平分线定理
    W_1 = CE + BE
    similar_ratio = D / D_0
    W_2 = W_1 * similar_ratio
    return D, W_2, W_1

sum_len=[]
for test_theta in theta:
    for line_d in np.arange(100,0,-0.01):
        D, W_2, W_1 = parallel_2(line_d,alpha_2*pi/180,D_1_min,test_theta)
        sum_len.append(W_1)
for test_theta in theta:
    for line_d in np.arange(800,300,-0.01):
        D, W_2, W_1 = parallel_1(line_d,alpha_1*pi/180,D_2_max,test_theta)
        sum_len.append(W_2)
print(sum(sum_len))