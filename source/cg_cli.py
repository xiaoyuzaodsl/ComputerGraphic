#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import cg_algorithms as alg
import numpy as np
from PIL import Image


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    item_dict = {}
    pen_color = np.zeros(3, np.uint8)
    width = 0
    height = 0

    with open(input_file, 'r') as fp:
        line = fp.readline()
        while line:
            line = line.strip().split(' ')
            # print(line)
            if line[0] == 'resetCanvas':
                width = int(line[1])
                height = int(line[2])
                item_dict = {}
            elif line[0] == 'saveCanvas':
                save_name = line[1]
                canvas = np.zeros([height, width, 3], np.uint8)
                canvas.fill(255)
                for item_type, p_list, algorithm, color in item_dict.values():
                    if item_type == 'line':
                        # print("draw a line")
                        pixels = alg.draw_line(p_list, algorithm)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                    elif item_type == 'polygon':
                        # print("draw a polygon")
                        pixels = alg.draw_polygon(p_list, algorithm)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                    elif item_type == 'ellipse':
                        # print("draw a ellipse")
                        pixels = alg.draw_ellipse(p_list)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                    elif item_type == 'circle':
                        # print("draw a circle")
                        pixels = alg.draw_circle(p_list)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                    elif item_type == 'curve':
                        # print("draw a curve")
                        pixels = alg.draw_curve(p_list, algorithm)
                        for x, y in pixels:
                            canvas[height - 1 - y, x] = color
                Image.fromarray(canvas).save(os.path.join(output_dir, save_name + '.bmp'), 'bmp')
            elif line[0] == 'setColor':
                pen_color[0] = int(line[1])
                pen_color[1] = int(line[2])
                pen_color[2] = int(line[3])
            elif line[0] == 'drawLine':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = line[6]
                item_dict[item_id] = ['line', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawPolygon':
                item_id = line[1]
                res_list = []
                i = 2
                max_len = len(line) - 2
                while i < max_len:
                    x = int(line[i])
                    y = int(line[i + 1])
                    i = i + 2
                    res_list.append([x, y])
                algorithm = line[len(line) - 1]
                item_dict[item_id] = ['polygon', res_list, algorithm, np.array(pen_color)]
            elif line[0] == 'drawEllipse':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = "ellipse"
                item_dict[item_id] = ['ellipse', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawCircle':
                item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                algorithm = "circle"
                item_dict[item_id] = ['circle', [[x0, y0], [x1, y1]], algorithm, np.array(pen_color)]
            elif line[0] == 'drawCurve':
                '''item_id = line[1]
                x0 = int(line[2])
                y0 = int(line[3])
                x1 = int(line[4])
                y1 = int(line[5])
                x2 = int(line[6])
                y2 = int(line[7])
                algorithm = line[8]
                '''
                item_id = line[1]
                res_list = []
                i = 2
                max_len = len(line) - 2
                while i < max_len:
                    x = int(line[i])
                    y = int(line[i + 1])
                    i = i + 2
                    res_list.append([x, y])
                algorithm = line[len(line) - 1]
                # print("res_list", res_list)
                item_dict[item_id] = ['curve', res_list, algorithm, np.array(pen_color)]

            elif line[0] == 'translate':
                item_id = line[1]
                dx = int(line[2])
                dy = int(line[3])
                old_item = item_dict[item_id]
                old_list = old_item[1]
                new_list = alg.translate(old_list, dx, dy)
                old_item[1] = new_list
                item_dict[item_id] = old_item
            elif line[0] == 'rotate':
                item_id = line[1]
                dx = int(line[2])
                dy = int(line[3])
                dr = int(line[4])
                old_item = item_dict[item_id]
                old_list = old_item[1]
                new_list = alg.rotate(old_list, dx, dy, dr)
                old_item[1] = new_list
                item_dict[item_id] = old_item
            elif line[0] == 'scale':
                item_id = line[1]
                dx = int(line[2])
                dy = int(line[3])
                ds = int(line[4])
                old_item = item_dict[item_id]
                old_list = old_item[1]
                new_list = alg.scale(old_list, dx, dy, ds)
                old_item[1] = new_list
                item_dict[item_id] = old_item
            elif line[0] == 'clip':
                item_id = line[1]
                x_min = int(line[2])
                y_min = int(line[3])
                x_max = int(line[4])
                y_max = int(line[5])
                algorithm = line[6]
                old_item = item_dict[item_id]
                old_list = old_item[1]
                new_list = alg.clip(old_list, x_min, y_min, x_max, y_max, algorithm)
                # print("new_list:", new_list)
                old_item[1] = new_list
                item_dict[item_id] = old_item

            line = fp.readline()

    # print(item_dict)