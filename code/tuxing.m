x=0:0.02:4;
y=0:0.02:5;
[x, y] = meshgrid(x,y);
[num]=xlsread('附件.xlsx', 'C3:GU253');
z=-num;

% 创建第一个图形窗口
figure(1)
% 绘制等高线图
[C,h] = contour(x, y, z);

% 获取每条等高线上的点的坐标
for i = 1:length(h.LevelList)
    level = h.LevelList(i);
    idx = find(C(1,:) == level);
    for j = 1:length(idx)
        start_idx = idx(j) + 1;
        end_idx = start_idx + C(2,idx(j)) - 1;
        xdata = C(1,start_idx:end_idx);
        ydata = C(2,start_idx:end_idx);
        disp(xdata)
        disp(ydata)
        % 在这里处理每条等高线上的点的坐标 (xdata, ydata)
    end
end


sc= meshc(x,y,z);
% sc(2).ZLocation = 'zmax';
xlabel('x')
ylabel('y')
zlabel('z')
grid on

% 增加等高线的密度
levels = 60; % 你可以根据需要调整这个值
contourf(x, y, z,  levels); % 创建填充的等高线图

% 添加颜色条
colorbar

% 输出第一张图片
print(1, '-dpng', 'figure1.png');

% 创建第二个图形窗口
figure(2)
mesh(x,y,z);
xlabel('x')
ylabel('y')
zlabel('z')
grid on

% 输出第二张图片
print(2, '-dpng', 'figure2.png');