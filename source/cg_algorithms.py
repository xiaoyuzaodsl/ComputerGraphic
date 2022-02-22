#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math
import numpy


def factorial(num):
    res = 1
    if num < 0:
         res = 0
    elif num == 0:
        res = 1
    else:
        for i in range(1, num + 1):
            res = i * res
    return res


def combination(n, i):
    res = 1
    res = factorial(n) / float((factorial(n - i) * factorial(i)))
    return res


def bezeir_coeffient(i, n, t):
    return combination(n, i) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, p_list):
    n = int(len(p_list)) - 1
    # print("n = ", n)
    x = y = 0
    for i in range(0, n + 1):
        p_x, p_y = p_list[i]
        # print("c(", n, i, ") = ", combination(n, i))
        bern_coff = bezeir_coeffient(i, n, t)
        x += p_x * bern_coff
        y += p_y * bern_coff
    return int(x), int(y)


def compute_code(x, y, x_min, y_min, x_max, y_max):
    code = 0
    if x < x_min:
        code |= 1   # left
    elif x > x_max:
        code |= 2   # right
    if y < y_min:
        code |= 4   # bottom
    elif y > y_max:
        code |= 8   # top
    return code


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
            for y in range(y1, y0 + 1):
                result.append((x0, y))
        else:
            k = (y1 - y0) / (x1 - x0)
            if abs(x1 - x0) > abs(y1 - y0):
                if x0 < x1:
                    x_step = 1
                    y_step = k
                else:
                    x_step = -1
                    y_step = -k
            else:
                if y0 < y1:
                    x_step = 1 / k
                    y_step = 1
                else:
                    x_step = -1 / k
                    y_step = -1
            x = x0
            y = y0
            if x0 < x1:
                while x <= x1:
                    result.append((int(x), int(y)))
                    x = x + x_step
                    y = y + y_step
            else:
                while x >= x1:
                    result.append((int(x), int(y)))
                    x = x + x_step
                    y = y + y_step
    elif algorithm == 'Bresenham':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
            for y in range(y1, y0 + 1):
                result.append((x0, y))
        else:
            x = x0
            y = y0
            if x1 > x0:
                x_dis = x1 - x0
            else:
                x_dis = x0 - x1
            if y1 > y0:
                y_dis = y1 - y0
            else:
                y_dis = y0 - y1
            if x0 < x1:
                x_step = 1
            else:
                x_step = -1
            if y0 < y1:
                y_step = 1
            else:
                y_step = -1
            if y_dis > x_dis:
                temp = x_dis
                x_dis = y_dis
                y_dis = temp
                interchange = 1
            else:
                interchange = 0
            e = 2 * y_dis - x_dis
            for i in range(1, x_dis):
                result.append([int(x),int(y)])
                while e > 0:
                    if interchange == 1:
                        x = x + x_step
                    else:
                        y = y + y_step
                    e = e - 2 * x_dis
                if interchange == 1:
                    y = y + y_step
                else:
                    x = x + x_step
                e = e + 2 * y_dis

    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    a = (x1 - x0) / 2
    b = (y0 - y1) / 2
    ct_x = (x0 + x1) / 2
    ct_y = (y0 + y1) / 2
    taa = a * a
    t2aa = taa * 2
    tbb = b * b
    t2bb = tbb * 2
    t2aabb = 2 * taa * tbb
    x = int(a + 1/2)
    y = 0
    while tbb * (x - 1/2) > taa * (y + 1):
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        d1 = tbb* (2*x*x - 2*x + 1/2) + t2aa*(y*y+2*y+1) - t2aabb
        if d1 < 0:
            y = y + 1
        else:
            x = x - 1
            y = y + 1
    d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    while x >= 0:
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        if d2 < 0:
            x = x - 1
            y = y + 1
        else:
            x = x - 1
        d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    return result


def draw_circle(p_list):
    """绘制圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    y1 = y0 - (x1 - x0)
    a = (x1 - x0) / 2
    b = (y0 - y1) / 2
    ct_x = (x0 + x1) / 2
    ct_y = (y0 + y1) / 2
    taa = a * a
    t2aa = taa * 2
    tbb = b * b
    t2bb = tbb * 2
    t2aabb = 2 * taa * tbb
    x = int(a + 1/2)
    y = 0
    while tbb * (x - 1/2) > taa * (y + 1):
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        d1 = tbb* (2*x*x - 2*x + 1/2) + t2aa*(y*y+2*y+1) - t2aabb
        if d1 < 0:
            y = y + 1
        else:
            x = x - 1
            y = y + 1
    d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    while x >= 0:
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        if d2 < 0:
            x = x - 1
            y = y + 1
        else:
            x = x - 1
        d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':  # 先试试由三个点控制的
        '''
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        x2, y2 = p_list[2]
        # px = (1-t)^2*p0 + 2t*(1-t)*p1 + t*2*p2 t为[0,1]
        dis = ((x1-x0)**2+(y1-y0)**2+(x2-x1)**2+(y2-y1)**2)**0.5
        dis = 1 / dis
        t = 0
        while t <= 1:
            x = ((1-t)**2)*x0+2*t*(1-t)*x1+(t**2)*x2
            y = ((1-t)**2)*y0+2*t*(1-t)*y1+(t**2)*y2
            result.append((int(x),int(y)))
            t = t + dis
            '''
        # x1 = x2 = 0
        # y1 = y2 = 0
        # print("p_list in curve", p_list)
        dis = 0
        for i in range(len(p_list)):
            x1, y1 = p_list[i-1]
            x2, y2 = p_list[i]
            dis += (x1 - x2) ** 2 + (y1 - y2)**2
        dis = dis ** 0.5
        if dis <= 0:
            return result
        dis = 1 / dis
        t = 0
        while t <= 1:
            # print(bezier(t, p_list))
            result.append(bezier(t, p_list))
            t += dis

        return result

    elif algorithm == 'B-spline': # 先写个四控制点试试吧
        '''
        x0, y0 = p_list[0]
        x1, y1 = p_list[1]
        x2, y2 = p_list[2]
        x3, y3 = p_list[3]
        dis = ((x1 - x0) ** 2 + (y1 - y0) ** 2 + (x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dis = 1 / dis
        t = 0
        while t <= 1:
            x = ((1-t)**3) * x0 + (3*t**3-6*t**2+4)*x1/6.0 + (-3*t**3+3*t**2+3*t+1)*x2/6.0+t**3*x3/6.0
            y = ((1-t)**3) * y0 + (3*t**3-6*t**2+4)*y1/6.0 + (-3*t**3+3*t**2+3*t+1)*y2/6.0+t**3*y3/6.0
            result.append(int(x), int(y))
            t += dis
            '''
        res_x = []
        res_y = []
        n = len(p_list) - 1
        k = 3
        u = numpy.linspace(1, 20, n + k + 1)

        def de_boor_x(r, t, i):
            if r == 0:
                x0, y0 = p_list[i]
                return x0
            else:
                if u[i+k-r] - u[i] == 0 and u[i+k-r]-u[i] != 0:
                    return ((u[i+k-r]-t)/(u[i+k-r]-u[i]))*de_boor_x(r-1, t, i-1)
                elif u[i+k-r] - u[i] != 0 and u[i+k-r]-u[i] == 0:
                    return ((u-t[i])/(u[i+k-r]-u[i]))*de_boor_x(r-1, t, i)
                elif u[i+k-r] - u[i] == 0 and u[i+k-r]-u[i] == 0:
                    return 0
                return ((t-u[i])/(u[i+k-r]-u[i]))*de_boor_x(r-1,t,i)+((u[i+k-r]-t)/(u[i+k-r]-u[i]))*de_boor_x(r-1,t,i-1)

        def de_boor_y(r, t, i):
            if r == 0:
                x0, y0 = p_list[i]
                return y0
            else:
                if u[i+k-r] - u[i] == 0 and u[i+k-r] - u[i] != 0:
                    return ((u[i+k-r]-t)/(u[i+k-r]-u[i]))*de_boor_y(r,t,i)
                elif u[i+k-r] - u[i] != 0 and u[i+k-r] - u[i] == 0:
                    return ((t-u[i])/(u[i+k-r]-u[i]))*de_boor_y(r,t,i)
                elif u[i+k-r] - u[i] == 0 and u[i+k-r] - u[i] == 0:
                    return 0
                return ((t-u[i])/(u[i+k-r]-u[i]))*de_boor_y(r-1,t,i)+((u[i+k-r]-t)/(u[i+k-r]-u[i]))*de_boor_y(r-1,t,i-1)
        dis = 0
        for m in range(len(p_list)):
            x0, y0 = p_list[m - 1]
            x1, y1 = p_list[m]
            dis = dis + ((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))**0.5
        if dis < 50:
            dis = 50
        dis = int(dis)
        if n >= k - 1:
            for j in range(k - 1, n + 1):
                for t in numpy.linspace(u[j], u[j + 1], dis):
                    res_x.append(int(de_boor_x(k - 1, t, j)))
                    res_y.append(int(de_boor_y(k - 1, t, j)))
        for i in range(len(res_x)):
            result.append((res_x[i], res_y[i]))
        # print("B-spline", result)
    return result


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        x, y = p_list[i]
        x = x + dx
        y = y + dy
        result.append((int(x), int(y)))
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # 注意书上是逆时针旋转
    result = []
    m = math.radians(r)
    for i in range(len(p_list)):
        x0, y0 = p_list[i]   # 用平移至原点+极坐标算出坐标关系
        # x1 = x + (x0 - x) * math.cos(m) - (y0 - y) * math.sin(m)
        # y1 = y + (x0 - x) * math.sin(m) + (y0 - y) * math.cos(m)
        x1 = x + (x0 - x) * math.cos(m) + (y0 - y) * math.sin(m)
        y1 = y - (x0 - x) * math.sin(m) + (y0 - y) * math.cos(m)
        result.append((int(x1), int(y1)))
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    # 平移至原点后缩放
    result = []
    for i in range(len(p_list)):
        x0, y0 = p_list[i]
        x1 = x0 * s + x * (1 - s)
        y1 = y0 * s + y * (1 - s)
        result.append((int(x1), int(y1)))
    return result


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 == x1:
        if x0 < x_min or x0 > x_max:
            return result
        if y0 > y1:
            x0, y0 = x1, y1
        if y0 > y_max or y1 < y_min:
            pass
        else:
            y1 = min(y1, y_max)
            y0 = max(y0, y_min)
            result.append((x0, y0))
            result.append((x1, y1))
        return result
    if y0 == y1:
        if y0 < y_min or y0 > y_max:
            return result
        if x0 > x1:
            x0, y0 = x1, y1
        if x0 > x_max or x1 < x_min:
            pass
        else:
            x0 = max(x0, x_min)
            x1 = min(x1, x_max)
            result.append((x0, y0))
            result.append((x1, y1))
        return result
    if algorithm == 'Cohen-Sutherland':

        code0 = compute_code(x0, y0, x_min, y_min, x_max, y_max)
        code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
        # print("code0 = ", code0, "code1 = ", code1)
        if (code0 | code1) == 0 : # 说明两个点都在0000区域
            result.append((x0,y0))    # 线段原样保留，不需要裁剪
            result.append((x1,y1))
        elif (code0 & code1) != 0 :
            pass    #线段直接丢弃，也不需要裁剪
        else:
            if x0 == x1:    # 直线斜率无穷大
                result.append((x0, y_min))
                result.append((x0, y_max))
            elif y1 == y0:  # 直线斜率为0
                result.append((x_min, y0))
                result.append((x_max, y0))
            else:
                k = (y1 - y0) / (x1 - x0)
                b = y0 - k * x0

                area = False    # 表示是否结束
                # print("in loop")
                while True:
                    # print("code0 = ", code0, "code1 = ", code1)
                    if (code0 | code1) == 0:       # 简取
                        area = True
                        break
                    elif (code0 & code1) != 0:      # 简弃
                        # area = False
                        break
                    out_code = 0
                    if code0 > code1:
                        out_code = code0
                    else:
                        out_code = code1
                    x = y = 0
                    # 下面按照左右上下的顺序一次裁剪线段
                    if (out_code & 1) != 0:    # 在窗口左侧
                        x = x_min
                        y = k*x_min + b
                    elif (out_code & 2) != 0:   # 在窗口右侧
                        x = x_max
                        y = k * x_max + b
                    elif (out_code & 4) != 0:   # 在窗口下
                        y = y_min
                        x = (y_min - b) / k
                    elif (out_code & 8) != 0:
                        y = y_max
                        x = (y_max - b) / k
                    if out_code == code0:
                        x0 = x
                        y0 = y
                        code0 = compute_code(x0, y0, x_min, y_min, x_max, y_max)
                    else:
                        x1 = x
                        y1 = y
                        code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
                if area == True:
                    # print("end : code0 = ", code0,"code1 =", code1)
                    result.append((int(x0), int(y0)))
                    result.append((int(x1), int(y1)))
    elif algorithm == 'Liang-Barsky':
        p1 = - (x1 - x0)
        q1 = x0 - x_min
        p2 = x1 - x0
        q2 = x_max - x0
        p3 = - (y1 - y0)
        q3 = y0 - y_min
        p4 = y1 - y0
        q4 = y_max - y0
        u1 = 0
        u2 = 1
        if p1 == 0:
            if x0 < x_max:
                if x0 > x_min:
                    result.append((x0, y_min))
                    result.append((x0, y_max))
        elif p3 == 0:
            if y0 < y_max:
                if y0 > y_min:
                    result.append((x_min, y0))
                    result.append((x_max, y0))
        # 负的p改u1，正的p改u2
        if p1 < 0:  # 说明 p2 > 0
            u1 = max(u1, q1 / p1)
            u2 = min(u2, q2 / p2)
        else:   # 说明p2 < 0
            u2 = min(u2, q1 / p1)
            u1 = max(u1, q2 / p2)
        if p3 < 0:
            u1 = max(u1, q3 / p3)
            u2 = min(u2, q4 / p4)
        else:
            u2 = min(u2, q3 / p3)
            u1 = max(u1, q4 / p4)
        if u1 < u2: # 反之直接舍弃
            x_0 = x0 + u1 * (x1 - x0)
            y_0 = y0 + u1 * (y1 - y0)
            x_1 = x0 + u2 * (x1 - x0)
            y_1 = y0 + u2 * (y1 - y0)
            result.append((int(x_0), int(y_0)))
            result.append((int(x_1), int(y_1)))
    # print("result = ", result)
    return result


def draw_control_point(point):
    """绘制圆（给定圆心，画一个半径为10的圆）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x, y = point
    x0, y0 = x - 10, y + 10
    x1, y1 = x + 10, y - 10
    y1 = y0 - (x1 - x0)
    a = (x1 - x0) / 2
    b = (y1 - y0) / 2
    ct_x = (x0 + x1) / 2
    ct_y = (y0 + y1) / 2
    taa = a * a
    t2aa = taa * 2
    tbb = b * b
    t2bb = tbb * 2
    t2aabb = 2 * taa * tbb
    x = int(a + 1/2)
    y = 0
    while tbb * (x - 1/2) > taa * (y + 1):
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        d1 = tbb* (2*x*x - 2*x + 1/2) + t2aa*(y*y+2*y+1) - t2aabb
        if d1 < 0:
            y = y + 1
        else:
            x = x - 1
            y = y + 1
    d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    while x >= 0:
        result.append((int(ct_x + x), int(ct_y + y)))
        result.append((int(ct_x - x), int(ct_y + y)))
        result.append((int(ct_x + x), int(ct_y - y)))
        result.append((int(ct_x - x), int(ct_y - y)))
        if d2 < 0:
            x = x - 1
            y = y + 1
        else:
            x = x - 1
        d2 = t2bb*(x*x - 2*x + 1) + taa*(2*y*y+2*y+1/2) - t2aabb
    return result


def scan_line(p_list, y):
    """
    :param p_list: 多变形的顶点序列
    :param y:   扫描线的y轴坐标
    :return:    扫描线
    """
    result = []
    vertex_id = 0
    for i in range(len(p_list)):
        x0, y0 = p_list[i - 1]
        x1, y1 = p_list[i]
        if (y - y0)*(y - y1) < 0:
            if x0 == x1:
                result.append([int(x0), int(y)])
            else:
                k = (y0 - y1) / (x0 - x1)
                if k == 0:
                    # 并不会执行
                    result.append([int(x0), int(y)])
                    result.append([int(x1), int(y)])
                else:
                    x = x0 + (y - y0) / k
                    result.append([int(x), int(y)])
        elif (y - y0)*(y - y1) == 0:
            # 本来想的是删去顶点求交时重复出现的顶点
            if y0 == y1:
                pass
            elif y - y0 == 0:
                if vertex_id == 0:
                    result.append([x0, y])
                    vertex_id = 1
                else:
                    result.append([x0, y])
                    vertex_id = 0
            elif y - y1 == 0:
                if vertex_id == 0:
                    result.append([x1, y])
                    vertex_id = 1
                else:
                    result.append([x1, y])
                    vertex_id = 0
    # print(result)
    return result


def my_insertion_sort(p_list):
    p_len = len(p_list)
    if p_len <= 0:
        return p_list
    # print("p_len = ", p_len)
    for i in range(1, p_len):
        end_x, end_y = p_list[i]
        # print("i = ", i)
        j = i - 1
        while j > -1:
            tmp_x, tmp_y = p_list[j]
            if tmp_x > end_x:
                p_list[j + 1] = [tmp_x, tmp_y]
            else:
                # p_list[j + 1] = [end_x, end_y]
                break
            j = j - 1
            # print(p_list)
            p_list[j + 1] = [end_x, end_y]
        # print(p_list)
    return p_list


def scan_fill_polygon(p_list):
    # 目前只针对凸多边形
    # 修正，现在有凹的也可以了，虽然有点瑕疵
    result = []
    x0, y0 = p_list[0]
    y_min = y0
    y_max = y0
    for i in range(len(p_list)):
        x1, y1 = p_list[i]
        y_min = min(y_min, y1)
        y_max = max(y_max, y1)
    # print("y_min = ", y_min, "and y_max = ", y_max)
    if y_max > 600:
        y_max = 600
    if y_min < 0:
        y_min = 0
    for y in range(y_min, y_max+1):
        tmp_list = scan_line(p_list, y)
        if len(tmp_list) < 2:
            pass
        elif len(tmp_list) == 2:
            x0, y0 = tmp_list[0]
            x1, y1 = tmp_list[1]
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            for x in range(x0, x1 + 1):
                result.append([int(x), int(y)])
        else:
            # 说明不止两个交点，已经不是凸多边形了
            # 先按照x坐标从小到大排序
            a_list = my_insertion_sort(tmp_list)
            # print(a_list)

            flag = len(a_list) % 2
            if flag == 0:
                for i in range(0, len(a_list) - 1, 2):
                    x0, y0 = a_list[i]
                    x1, y1 = a_list[i+1]
                    if x0 == x1 and y0 == y1:
                        if i < len(a_list) - 2:
                            x2, y2 = a_list[i+2]
                            x3, y3 = a_list[i+3]
                            if x2 == x3 and y2 == y3:
                                # 这时候说明问题大了
                                for x in range(x1, x2+1):
                                    result.append([int(x),int(y)])
                    else:
                        for x in range(x0, x1 + 1):
                            result.append([int(x), int(y)])
            else:
                for i in range(len(a_list) - 1):
                    x0, y0 = a_list[i]
                    x1, y1 = a_list[i+1]
                    for x in range(x0, x1 + 1):
                        result.append([int(x), int(y)])
    # print(result)
    return result


def seed_fill_ellipse(p_list):
    result = []
    N = numpy.zeros([600, 600])

    def seed_fill_zero(x, y, taa, tbb, taabb):
        if N[x, y] == 1 or tbb*x*x+taa*y*y - taabb > 0:
            return
        if tbb*x*x+taa*y*y - taabb < 0:
            result.append([x, y])
            N[x, y] = 1
            seed_fill_zero(x+1, y, taa, tbb, taabb)
            seed_fill_zero(x, y+1, taa, tbb, taabb)

    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    a = (x1 - x0) / 2
    b = (y1 - y0) / 2
    xm = (x1 + x0) / 2
    ym = (y1 + y0) / 2
    t1aa = a*a
    t1bb = b*b
    t1aabb = t1aa * t1bb
    # print("a = ", a, "b = ", b)
    seed_fill_zero(0, 0, t1aa, t1bb, t1aabb)
    true_res = []
    for i in range(len(result)):
        x, y = result[i]
        true_res.append([int(xm + x), int(ym + y)])
        true_res.append([int(xm + x), int(ym - y)])
        true_res.append([int(xm - x), int(ym - y)])
        true_res.append([int(xm - x), int(ym + y)])
    return true_res


def clip_polygon(p_list, x_min, y_min, x_max, y_max):
    # 目前只打算支持多边形
    def clip_point(outcode, bounding): # 0,1,2,3->左右下上
        res = 1     # res = 1时候表示在内部
        if bounding == 0:
            if (outcode & 1) != 0:
                res = 0
        elif bounding == 1:
            if (outcode & 2) != 0:
                res = 0
        elif bounding == 2:
            if (outcode & 4) != 0:
                res = 0
        elif bounding == 3:
            if (outcode & 8) != 0:
                res = 0
        else:
            pass
        return res

    a_list = p_list
    for k in range(4):
        tmp_list = []
        for i in range(len(a_list)):
            x0, y0 = a_list[i - 1]
            x1, y1 = a_list[i]
            outcode0 = compute_code(x0, y0, x_min, y_min, x_max, y_max)
            outcode1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
            clip0 = clip_point(outcode0, k)
            clip1 = clip_point(outcode1, k)
            if clip0 == 0 and clip1 == 0:
                pass
            elif clip0 == 0 and clip1 == 1:
                # 加两个点
                if x0 == x1:
                    if k == 2:  # 下
                        tmp_list.append([x0, y_min])
                        tmp_list.append([x1, y1])
                    elif k == 3:    # 上
                        tmp_list.append([x0, y_max])
                        tmp_list.append([x1, y1])
                    else:   # 不应该存在
                        pass
                else:
                    kl = (y0 - y1) / (x0 - x1)
                    b = y0 - kl * x0
                    if k == 0:  #左
                        y = kl * x_min + b
                        tmp_list.append([int(x_min), int(y)])
                        tmp_list.append([x1, y1])
                    elif k == 1:    #右
                        y = kl * x_max + b
                        tmp_list.append([int(x_max), int(y)])
                        tmp_list.append([x1, y1])
                    elif k == 2:    #下
                        if kl == 0:
                            pass
                        else:
                            x = (y_min - b) / kl
                            tmp_list.append([int(x), int(y_min)])
                            tmp_list.append([x1, y1])
                    elif k == 3:    #上
                        if kl == 0:
                            pass
                        else:
                            x = (y_max - b) / kl
                            tmp_list.append([int(x), int(y_max)])
                            tmp_list.append([x1, y1])
            elif clip0 == 1 and clip1 == 0:
                # 加一个交点
                if x0 == x1:
                    if k == 2:  # 下
                        tmp_list.append([x0, y_min])
                    elif k == 3:    # 上
                        tmp_list.append([x0, y_max])
                    else:   # 不应该存在
                        pass
                else:
                    kl = (y0 - y1) / (x0 - x1)
                    b = y0 - kl * x0
                    if k == 0:  #左
                        y = kl * x_min + b
                        tmp_list.append([int(x_min), int(y)])
                    elif k == 1:    #右
                        y = kl * x_max + b
                        tmp_list.append([int(x_max), int(y)])
                    elif k == 2:    #下
                        if kl == 0:
                            pass
                        else:
                            x = (y_min - b) / kl
                            tmp_list.append([int(x), int(y_min)])
                    elif k == 3:    #上
                        if kl == 0:
                            pass
                        else:
                            x = (y_max - b) / kl
                            tmp_list.append([int(x), int(y_max)])
            else:
                # 加一个顶点(第二个)
                tmp_list.append([x1, y1])
        a_list = tmp_list
    return a_list
