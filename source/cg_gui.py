#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import cg_algorithms as alg
from typing import Optional
import math
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QColorDialog,
    QMessageBox,
    QInputDialog,
    QAction)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor, QImage, QPen, QIcon
from PyQt5.QtCore import QRectF, Qt, QSize


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.click = 0
        self.color = QColor(0, 0, 0)
        self.pen_size = 1
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.fill = 0
        self.fill_color = QColor(0, 255, 0)
        self.setMouseTracking(True)

    def start_reset(self):
        # print("item_dict", self.item_dict)
        # print("list_widget", self.list_widget)
        for items, me in self.item_dict.items():
            # print(items, "\t", self.item_dict[items])
            self.scene().removeItem(me)
        if self.click != 0: # 说明画到一半重置了，有够变态
            self.scene().removeItem(self.temp_item)
        self.item_dict.clear()
        self.updateScene([self.sceneRect()])
        self.click = 0

        self.status = ''
        self.click = 0
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.click = 0

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.click = 0

    def start_draw_ellipse(self, algorithm, item_id):
        self.status = 'ellipse'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.click = 0

    def start_draw_circle(self, algorithm, item_id):
        self.status = 'circle'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.click = 0

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.click = 0

    def start_translate(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要平移的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            self.status = 'translate'
            self.temp_id = self.selected_id
        self.click = 0

    def start_rotate(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要旋转的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            self.status = 'rotate'
            self.temp_id = self.selected_id
        self.click = 0

    def start_scale(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要缩放的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            self.status = 'scale'
            self.temp_id = self.selected_id
        self.click = 0

    def start_clip_polygon(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要裁剪的多边形",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            self.status = 'clip_polygon'
            self.temp_algorithm = 'sutherland-hodgman'
            self.temp_id = self.selected_id
        self.click = 0

    def start_clip_cohen_sutherland(self, algorithm):
        if self.selected_id == '' or self.item_dict[self.selected_id].item_type!='line':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要裁剪的线段",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            self.status = 'clip'
            self.temp_algorithm = algorithm
            self.temp_id = self.selected_id
        self.click = 0

    def start_clip_liang_barsky(self, algorithm):
        if self.selected_id == '' or self.item_dict[self.selected_id].item_type!= 'line':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要裁剪的线段",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            self.status = 'clip'
            self.temp_algorithm = algorithm
            self.temp_id = self.selected_id
        self.click = 0

    def start_remove_item(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要删除的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            me = self.item_dict[self.selected_id]
            self.scene().removeItem(me)
            self.updateScene([self.sceneRect()])
            list_me = self.list_widget.currentItem()
            self.list_widget.takeItem(self.list_widget.row(list_me))
            """
            self.temp_algorithm = ''
            self.temp_id = ''
            self.temp_item = None
            self.selected_id = ''
            self.status = ''
            """

    def start_copy_item(self, item_id):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要拷贝的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            self.temp_id = item_id

            me = self.item_dict[self.selected_id]
            self.status = me.item_type
            self.temp_algorithm = me.algorithm
            # print(item_id, me.item_type, me.p_list, me.algorithm,
            #    me.color, me.pen_size, me.fill, me.fill_color)
            self.temp_item = MyItem(item_id, self.status, me.p_list,
                                    self.temp_algorithm,
                                    me.color, me.pen_size, me.fill, me.fill_color)
            # print(me)
            # print(self.temp_item)
            # print(self.temp_item.id)
            self.item_dict[self.temp_id] = self.temp_item
            self.scene().addItem(self.temp_item)
            self.list_widget.addItem(item_id)
            self.finish_draw()
            self.updateScene([self.sceneRect()])
            # print("list_widget: ", self.list_widget)
            # print("item_dict", self.item_dict)
            self.click = 0
            self.selected_id = ''

    def start_fill(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要填充的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            me = self.item_dict[self.selected_id]
            me.fill = 1
            me.fill_color = self.fill_color
            self.updateScene([self.sceneRect()])

    def fill_clear(self):
        if self.selected_id == '':
            QMessageBox.warning(self, 'CG 2020', "请确认已选择需要取消填充的图元",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            pass
        else:
            me = self.item_dict[self.selected_id]
            me.fill = 0
            # me.fill_color = self.fill_color
            self.updateScene([self.sceneRect()])

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        self.click = 0

    def clear_selection(self):
        if self.item_dict:
            if self.selected_id != '':
                self.item_dict[self.selected_id].selected = False
                self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.list_widget.currentItem():
            if self.selected_id != '' and self.selected_id in self.item_dict.keys():
                self.item_dict[self.selected_id].selected = False
                self.item_dict[self.selected_id].update()

            self.selected_id = selected
            self.item_dict[selected].selected = True
            self.item_dict[selected].update()
            self.status = ''

        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.click == 0:
            if self.status == 'line':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        self.color, self.pen_size, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'ellipse':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        self.color, self.pen_size, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'circle':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        self.color, self.pen_size, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'polygon':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        self.color, self.pen_size, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'curve':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        self.color, self.pen_size, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'translate':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, 1)
                # self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            elif self.status == 'rotate':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y + 20]], self.temp_algorithm, 1)
                # self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
                point_num = len(self.item_dict[self.selected_id].p_list)
                # print(self.temp_item.p_list)
                for i in range(point_num):
                    x0, y0 = self.item_dict[self.selected_id].p_list[i]
                    self.temp_item.p_list.append([x0, y0])
            elif self.status == 'scale':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, 1)
                # self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
                point_num = len(self.item_dict[self.selected_id].p_list)
                # print(self.temp_item.p_list)
                for i in range(point_num):
                    x0, y0 = self.item_dict[self.selected_id].p_list[i]
                    self.temp_item.p_list.append([x0, y0])
            elif self.status == 'clip' or self.status == 'clip_polygon':
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm,
                                        QColor(255, 0, 0), 1, 1)
                self.scene().addItem(self.temp_item)
                self.updateScene([self.sceneRect()])
            self.click += 1
        else:
            if self.status == 'line':
                self.temp_item.p_list[1] = [x, y]
                self.temp_item.being_draw = 0
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
                self.click = 0
            elif self.status == 'ellipse':
                self.temp_item.p_list[1] = [x, y]
                self.temp_item.being_draw = 0
                self.click = 0
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
            elif self.status == 'circle':
                x0, y0 = self.temp_item.p_list[0]
                if (x - x0) * (y - y0) < 0:
                    self.temp_item.p_list[1] = [x, y0 - (x - x0)]
                else:
                    self.temp_item.p_list[1] = [x, y0 + (x - x0)]
                self.temp_item.being_draw = 0
                self.click = 0
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()
            elif self.status == 'polygon':
                x0, y0 = self.temp_item.p_list[0]
                dis = (x - x0) * (x - x0) + (y - y0) * (y - y0)
                if dis < 100:
                    polygon_tmp_num = len(self.temp_item.p_list)
                    self.temp_item.p_list[polygon_tmp_num - 1] = [x0, y0]
                    del self.temp_item.p_list[polygon_tmp_num - 1]
                    self.temp_item.being_draw = 0
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.click = 0
                else:
                    self.temp_item.p_list.append([x, y])
                    self.click += 1
            elif self.status == 'curve':
                control_point_num = len(self.temp_item.p_list)
                self.temp_item.p_list[control_point_num - 1] = (x, y)
                self.temp_item.p_list.append((x, y))
                self.click += 1
            elif self.status == 'translate':
                x0, y0 = self.temp_item.p_list[0]
                self.item_dict[self.selected_id].p_list = alg.translate(self.item_dict[self.selected_id].p_list, x - x0, y - y0)
                self.temp_item.p_list[0] = (x, y)
                self.finish_draw()
                self.click = 0
            elif self.status == 'rotate':
                self.finish_draw()
                self.click = 0
            elif self.status == 'scale':
                self.finish_draw()
                self.click = 0
            elif self.status == 'clip':
                self.temp_item.p_list[1] = [x, y]
                x0, y0 = self.temp_item.p_list[0]
                x1, y1 = self.temp_item.p_list[1]
                x_min = min(x0, x1)
                x_max = max(x0, x1)
                y_min = min(y0, y1)
                y_max = max(y0, y1)
                self.item_dict[self.selected_id].p_list = alg.clip(self.item_dict[self.selected_id].p_list,
                                                                   x_min, y_min, x_max, y_max, self.temp_algorithm)
                self.scene().removeItem(self.temp_item)
                if len(self.item_dict[self.selected_id].p_list) == 0:
                    pass
                self.click = 0
            elif self.status == 'clip_polygon':
                self.temp_item.p_list[1] = [x, y]
                x0, y0 = self.temp_item.p_list[0]
                x1, y1 = self.temp_item.p_list[1]
                x_min = min(x0, x1)
                x_max = max(x0, x1)
                y_min = min(y0, y1)
                y_max = max(y0, y1)
                self.item_dict[self.selected_id].p_list = alg.clip_polygon(self.item_dict[self.selected_id].p_list,
                                                                   x_min, y_min, x_max, y_max)
                self.scene().removeItem(self.temp_item)
                if len(self.item_dict[self.selected_id].p_list) == 0:
                    pass
                self.click = 0
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.click == 0:
            pass
        else:
            if self.status == 'line':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'polygon':
                polygon_tmp_num = len(self.temp_item.p_list)
                self.temp_item.p_list[polygon_tmp_num - 1] = [x, y]
            elif self.status == 'ellipse':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'circle':
                x0, y0 = self.temp_item.p_list[0]
                if (x - x0) * (y - y0) < 0:
                    self.temp_item.p_list[1] = [x, y0 - (x - x0)]
                else:
                    self.temp_item.p_list[1] = [x, y0 + (x - x0)]
            elif self.status == 'curve':
                control_point_num = len(self.temp_item.p_list)
                self.temp_item.p_list[control_point_num - 1] = [x, y]
            elif self.status == 'translate':
                x0, y0 = self.temp_item.p_list[0]
                self.item_dict[self.selected_id].p_list = alg.translate(self.item_dict[self.selected_id].p_list, x - x0, y - y0)
                self.temp_item.p_list[0] = [x, y]
            elif self.status == 'rotate':
                xr, yr = self.temp_item.p_list[0]
                x0, y0 = self.temp_item.p_list[1]
                a = ((x - xr) * (x - xr) + (y - yr) * (y - yr))**0.5
                b = ((x0 - xr) * (x0 - xr) + (y0 - yr) * (y0 - yr))**0.5
                c = ((x - x0) * (x - x0) + (y - y0) * (y - y0))**0.5
                if a == 0 or b == 0 or c == 0:
                    pass
                else:
                    # print("a b c", a, b, c)
                    cos_c = (a*a + b*b - c*c) / (2 * a * b)
                    rotation = math.degrees(math.acos(cos_c))
                    # 这里需要特判一下逆时针旋转角是不是会大于180度,因为0-360同一个cos对应两个值
                    # 默认的转轴为 x = x0
                    x0, y0 = self.temp_item.p_list[0]
                    if x < x0:
                        rotation = 360 - rotation
                    # print("cos(c)", cos_c, "rotation", rotation)
                    tmp_list = self.temp_item.p_list[2:]
                    self.item_dict[self.selected_id].p_list = alg.rotate(tmp_list, xr, yr, rotation)
            elif self.status == 'scale':
                xs, ys = self.temp_item.p_list[0]
                dis = ((x - xs)*(x - xs) + (y - ys)*(y - ys))*0.5
                # print("dis = ", dis)
                s = dis / 400
                tmp_list = self.temp_item.p_list[2:]
                self.item_dict[self.selected_id].p_list = alg.scale(tmp_list, xs, ys, s)
            elif self.status == 'clip' or self.status == 'clip_polygon':
                self.temp_item.p_list[1] = [x, y]
        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.click == 0:
            pass
        else:
            self.temp_item.being_draw = 0
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            # print(self.item_dict[self.temp_id].algorithm)
            self.finish_draw()
            self.click = 0


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '',
                 color: QColor = QColor(0, 0, 0), pen_size: int = 1,
                 being_draw: int = 0,
                 fill: int = 0,
                 fill_color: QColor = QColor(0, 255, 0),
                 parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        self.color = color
        self.pen_size = pen_size
        self.being_draw = being_draw
        self.fill = fill
        self.fill_color = fill_color

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(QPen(self.color, self.pen_size))
        if self.being_draw == 1:
            painter.setPen(QColor(255, 0, 0))
            for con_pt in self.p_list:
                con_pt_pixels = alg.draw_control_point(con_pt)
                for p in con_pt_pixels:
                    painter.drawPoint(*p)
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            painter.setPen(QPen(self.color, self.pen_size))
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                for con_pt in self.p_list:
                    con_pt_pixels = alg.draw_control_point(con_pt)
                    for p in con_pt_pixels:
                        painter.drawPoint(*p)
        elif self.item_type == 'polygon':
            painter.setPen(QPen(self.color, self.pen_size))
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                for con_pt in self.p_list:
                    con_pt_pixels = alg.draw_control_point(con_pt)
                    for p in con_pt_pixels:
                        painter.drawPoint(*p)
            if self.fill == 1:
                painter.setPen(QPen(self.fill_color, self.pen_size))
                fill_pixels = alg.scan_fill_polygon(self.p_list)
                for p in fill_pixels:
                    x0, y0 = p
                    if 0 <= x0 <= 600 and 0 <= y0 <=600:
                        painter.drawPoint(*p)
        elif self.item_type == 'ellipse':
            painter.setPen(QPen(self.color, self.pen_size))
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            if x0 > x1:
                x0, x1 = x1, x0
            if y0 < y1:
                y0, y1 = y1, y0
            item_pixels = alg.draw_ellipse(([x0, y0], [x1, y1]))
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                for con_pt in self.p_list:
                    con_pt_pixels = alg.draw_control_point(con_pt)
                    for p in con_pt_pixels:
                        painter.drawPoint(*p)
            if self.fill == 1:
                painter.setPen(QPen(self.fill_color, self.pen_size))
                fill_pixels = alg.seed_fill_ellipse(self.p_list)
                for p in fill_pixels:
                    x0, y0 = p
                    if 0 <= x0 <= 600 and 0 <= y0 <=600:
                        painter.drawPoint(*p)
        elif self.item_type == 'circle':
            painter.setPen(QPen(self.color, self.pen_size))
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            if x0 > x1:
                x0, x1 = x1, x0
            if y0 < y1:
                y0, y1 = y1, y0
            item_pixels = alg.draw_circle(([x0, y0], [x1, y1]))
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                for con_pt in self.p_list:
                    con_pt_pixels = alg.draw_control_point(con_pt)
                    for p in con_pt_pixels:
                        painter.drawPoint(*p)
            if self.fill == 1:
                painter.setPen(QPen(self.fill_color, self.pen_size))
                fill_pixels = alg.seed_fill_ellipse(self.p_list)
                for p in fill_pixels:
                    x0, y0 = p
                    if 0 <= x0 <= 600 and 0 <= y0 <=600:
                        painter.drawPoint(*p)
        elif self.item_type == 'curve':
            painter.setPen(QPen(self.color, self.pen_size))
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
                for con_pt in self.p_list:
                    con_pt_pixels = alg.draw_control_point(con_pt)
                    for p in con_pt_pixels:
                        painter.drawPoint(*p)
        elif self.item_type == 'clip' or 'clip_polygon':
            painter.setPen(QPen(QColor(255, 0, 0),1))
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x_min = min(x0, x1)
            x_max = max(x0, x1)
            y_min = min(y0, y1)
            y_max = max(y0, y1)
            item_pixels = alg.draw_polygon(([x_min, y_min], [x_max, y_min],
                                            [x_max, y_max], [x_min, y_max], [x_min, y_min]), "Bresenham")
            for p in item_pixels:
                painter.drawPoint(*p)

    def boundingRect(self) -> QRectF:
        if len(self.p_list) == 0:
            return QRectF(0, 0, 0, 0)

        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            point_num = len(self.p_list)
            # print(self.p_list)
            x, y = self.p_list[0]
            w, h = self.p_list[0]
            for i in range(point_num):
                x0, y0 = self.p_list[i]
                x = min(x, x0)
                y = min(y, y0)
                w = max(w, x0)
                h = max(h, y0)
            # print("x y w h", x, y, w, h)
            w = w - x
            h = h - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'circle':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = max(y0, y1) - (max(x0, x1) - x)
            w = max(x0, x1) - x
            h = w
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            point_num = len(self.p_list)
            x, y = self.p_list[0]
            w, h = self.p_list[0]
            for i in range(point_num):
                x0, y0 = self.p_list[i]
                x = min(x, x0)
                y = min(y, y0)
                w = max(w, x0)
                h = max(h, y0)
            w -= x
            h -= y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'clip' or 'clip_polygon':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = max(y0, y1) - (max(x0, x1) - x)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget
        # self.save_name = 1

        # 设置图标
        self.setWindowIcon(QIcon('icon/title_icon.png'))
        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')

        # save_canvas_act = file_menu.addAction('保存画布')
        # reset_canvas_act = file_menu.addAction('重置画布')
        # exit_act = file_menu.addAction('退出')
        save_canvas_act = QAction(QIcon('icon/save_icon.png'), '&保存画布', self)
        reset_canvas_act = QAction(QIcon('icon/reset_icon.png'), '&重置画布', self)
        exit_act = QAction(QIcon('icon/exit_icon.png'), '&退出', self)
        file_menu.addAction(save_canvas_act)
        file_menu.addAction(reset_canvas_act)
        file_menu.addAction(exit_act)
        save_canvas_act.setShortcut('Shift+Ctrl+S')
        reset_canvas_act.setShortcut('Ctrl+W')
        exit_act.setShortcut('Ctrl+Q')

        set_pen = menubar.addMenu('画笔')
        set_pen_color_act = set_pen.addAction('画笔颜色')
        set_pen_size = set_pen.addMenu('画笔粗细')
        set_pen_size_act1 = QAction(QIcon('icon/pen_1.png'), '&画笔1', self)
        set_pen_size_act2 = QAction(QIcon('icon/pen_2.png'), '&画笔2', self)
        set_pen_size_act3 = QAction(QIcon('icon/pen_3.png'), '&画笔3', self)
        set_pen_size.addAction(set_pen_size_act1)
        set_pen_size.addAction(set_pen_size_act2)
        set_pen_size.addAction(set_pen_size_act3)

        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        circle_act = draw_menu.addAction('圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')

        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪线段')
        clip_polygon_act = edit_menu.addAction('裁剪多边形')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')
        remove_item_act = edit_menu.addAction('删除图元')
        copy_item_act = edit_menu.addAction('复制图元')

        fill_menu = menubar.addMenu('填充')
        fill_act = fill_menu.addAction('填充图元')
        fill_color_act = fill_menu.addAction('填充颜色')
        fill_clear_color_act = fill_menu.addAction('取消填充')

        # 连接信号和槽函数
        exit_act.triggered.connect(self.close)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        set_pen_color_act.triggered.connect(self.set_pen_color_action)
        set_pen_size_act1.triggered.connect(self.set_pen_size_action)
        set_pen_size_act2.triggered.connect(self.set_pen_size_action)
        set_pen_size_act3.triggered.connect(self.set_pen_size_action)

        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        circle_act.triggered.connect(self.circle_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_polygon_act.triggered.connect(self.clip_polygon_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        remove_item_act.triggered.connect(self.remove_item_action)
        copy_item_act.triggered.connect(self.copy_item_action)
        fill_act.triggered.connect(self.fill_action)
        fill_color_act.triggered.connect(self.fill_color_action)
        fill_clear_color_act.triggered.connect(self.fill_clear_color_action)

        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG 2020')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'CG 2020',
                                     "是否确认退出?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def save_canvas_action(self):
        self.statusBar().showMessage('快速保存为bmp文件')
        text, ok = QInputDialog.getText(self, 'CG 2020',
                                        '输入需要保存的文件名:')
        if ok:
            rect_f = self.scene.sceneRect()
            img = QImage(QSize(600, 600), QImage.Format_RGB888)
            img.fill(Qt.white)
            p = QPainter(img)
            self.scene.render(p, target=QRectF(img.rect()), source=rect_f)
            p.end()
            saving = img.save('output/' + str(text) + '.bmp')
            # self.save_name += 1
            print("saving pass" if saving else "saving not pass")

    def reset_canvas_action(self):
        reply = QMessageBox.question(self, 'CG 2020',
                                     "是否确认清空画布?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.item_cnt = 0
            self.canvas_widget.start_reset()
            self.list_widget.clear()
            self.statusBar().showMessage('重置')
        else:
            pass

    def set_pen_color_action(self):
        col = QColor(0, 0, 0)
        tmp_color = QColorDialog.getColor()
        if tmp_color.isValid():
            col = tmp_color
        self.canvas_widget.color = col

    def set_pen_size_action(self):
        pen_size = 1
        sender = self.sender()
        # print(sender.text())
        if sender.text() == '&画笔1':
            pen_size = 1
        elif sender.text() == '&画笔2':
            pen_size = 3
        elif sender.text() == '&画笔3':
            pen_size = 5
        else:
            pen_size = 1
        self.canvas_widget.pen_size = pen_size

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse('ellipse', self.get_id())
        self.statusBar().showMessage('绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def circle_action(self):
        self.canvas_widget.start_draw_circle('circle', self.get_id())
        self.statusBar().showMessage('绘制圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转')

    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放')

    def clip_polygon_action(self):
        self.canvas_widget.start_clip_polygon()
        self.statusBar().showMessage('Sutherland-Hodgman裁剪多边形')

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip_cohen_sutherland("Cohen-Sutherland")
        self.statusBar().showMessage('Cohen-Sutherland裁剪视图')

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip_liang_barsky("Liang-Barsky")
        self.statusBar().showMessage('Liang-Barsky裁剪视图')

    def remove_item_action(self):
        self.canvas_widget.start_remove_item()
        self.statusBar().showMessage("删除图元")

    def copy_item_action(self):
        self.canvas_widget.start_copy_item(self.get_id())
        self.statusBar().showMessage("复制图元")

    def fill_action(self):
        self.canvas_widget.start_fill()
        self.statusBar().showMessage("填充图元")

    def fill_color_action(self):
        col = QColor(0, 0, 0)
        tmp_color = QColorDialog.getColor()
        if tmp_color.isValid():
            col = tmp_color
        self.canvas_widget.fill_color = col
        self.statusBar().showMessage("填充图元")

    def fill_clear_color_action(self):
        self.canvas_widget.fill_clear()
        self.statusBar().showMessage("取消填充图元")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
