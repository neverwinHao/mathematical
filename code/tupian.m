% 随机生成一组（x,y,z),这些点的坐标离一个空间平面比较近
x=0:0.2:5;
y=0:0.2:4;
[x, y] = meshgrid(x,y);

[num]=xlsread('附件.xlsx', 'C3:GU253');
point_left = [];
point_right = [];

z=-num;
for i = 1:numel(x)
    if (250/57.0)*x(i) - (590/57.0) < y(i)
        point_left = [point_left; x(i), y(i), z(i)];
    else
        point_right = [point_right; x(i), y(i), z(i)];
    end
end

x_left=point_left(:,1);
y_left=point_left(:,2);
z_left=point_left(:,3);

x_right=point_right(:,1);
y_right=point_right(:,2);
z_right=point_right(:,3);

disp(x_left)

X = [ones(length(x_left),1) x_left y_left];

% 拟合，其实是线性回归，但可以用来拟合平面
% 输出为 b = [b(1) b(2) b(3)] 表示 z = b(1) + b(2)*x + b(3)*y 是拟合出来的平面的方程
[b1,bint,r,rint,stats] = regress(z_left,X,0.05);
disp(b1)

X = [ones(length(x_right),1) x_right y_right];

% 拟合，其实是线性回归，但可以用来拟合平面
% 输出为 b = [b(1) b(2) b(3)] 表示 z = b(1) + b(2)*x + b(3)*y 是拟合出来的平面的方程
[b2,bint,r,rint,stats] = regress(z_right,X,0.05);
disp(b2)

% 
% % 定义两个平面的方程
% z1 = b1(1) - b1(2).*x - b1(3).*y;
% z2 = b2(1) - b2(2).*x + b2(3).*y;

% 定义两个平面的方程
z1 = -13.6401 - 8.4891.*x - 8.7826.*y;
z2 = 53.3796 - 55.4623.*x + 18.6960.*y;

% 计算两个平面的交点
z_intersect = min(z1, z2);

% 绘制两个平面
figure
surf(x, y, z1, 'FaceColor', 'r', 'FaceAlpha', 0.5);
hold on
surf(x, y, z2, 'FaceColor', 'b', 'FaceAlpha', 0.5);

% 隐藏两个平面相对上方的部分
z1(z1 > z_intersect) = NaN;
z2(z2 > z_intersect) = NaN;
surf(x, y, z1, 'FaceColor', 'r', 'FaceAlpha', 0.5);
surf(x, y, z2, 'FaceColor', 'b', 'FaceAlpha', 0.5);

hold off

xlabel('x/海里')
ylabel('y/海里')
zlabel('z/米')