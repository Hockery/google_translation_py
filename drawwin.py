
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QCursor, QBitmap
from PyQt5.QtCore import Qt, QPoint
from qtpy.QtGui import QPen, QColor


class ShapeWidget(QWidget):
    def __init__(self, parent=None):
        super(ShapeWidget, self).__init__(parent)
        self.setWindowTitle("不规则的，可以拖动的窗体实现例子")
        self.createMode = 'doodle_contour'
        # self.mypix()
        self.width  = 0
        self.height = 0
        self.radius = 0
        self.set_window(300,300,10)
    def set_width(self, width):
        if not isinstance(width, int) or width < 0:
            return False
        self.width = width
        return True 
    def set_height(self, height):
        if not isinstance(height, int) or height < 0:
            return False
        self.height = height
        return True
    def set_radius(self, radius):
        min_size = self.height if self.width > self.height else self.width
        if radius > min_size/2:
            radius =min_size/2
        self.radius = radius
        return True
    def set_window(self, width, height,radius):
        if not self.set_width(width):
            print('width must be a integer which greater than 0 ')
        if not self.set_height(height):
            print('height must be a integer which greater than 0 ')
        self.set_radius(radius)

        #获得图片自身的遮罩
        back_mask=self.get_mask()
        if back_mask is None:
            print("error back_mask")
            return False
        #将获得的图片的大小作为窗口的大小
        self.resize(back_mask.size())
        #增加一个遮罩
        self.setMask(back_mask)
        #print(self.pix.size())
        self.dragPosition = None
        return True
    def draw_radius(self, painter):
        painter.setPen(QPen(QColor(0, 0, 0, 0), 0))
        # 1
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0,0,self.radius,self.radius)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(QPoint(self.radius,self.radius),self.radius,self.radius)
        # 2
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(self.width-self.radius,0,self.radius,self.radius)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(QPoint(self.width-self.radius,self.radius),self.radius,self.radius)
        # 3
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0,self.height-self.radius,self.radius,self.radius)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(QPoint(self.radius,self.height-self.radius),self.radius,self.radius)
        # 4
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(self.width-self.radius,self.height-self.radius,self.radius,self.radius)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(QPoint(self.width-self.radius,self.height-self.radius),self.radius,self.radius)

    def get_mask(self):
        _doodle_painter = QPainter()
        self.doodle_pixmap = QBitmap(self.width, self.height)
        self.doodle_pen_size = 4
        doodle_p = _doodle_painter
        doodle_p.begin(self.doodle_pixmap) #.doodle_pixmap
        doodle_p.setRenderHint(QPainter.Antialiasing)
        doodle_p.setRenderHint(QPainter.HighQualityAntialiasing)
        doodle_p.setRenderHint(QPainter.SmoothPixmapTransform)
        # --------------------解决点击没反应的问题--------------------
        doodle_p.setPen(QPen(QColor(0, 0, 0, 0), 0))
        if self.createMode == 'doodle_contour':
            doodle_p.setBrush(QColor(0, 0, 0))
        else: 
            doodle_p.setBrush(QColor(255, 255, 255))
        # if self.cur_pos != None:
        #     print("point:", self.cur_pos)
        #     doodle_p.drawEllipse(self.cur_pos, self.radius/2, self.radius/2) 
        # ----------------------------------------------------------
        # doodle_p.setBrush(QColor(255, 255, 255))
        # doodle_p.drawRect(0, 0, 100, 100)
        doodle_p.setBrush(QColor(0, 0, 0))
        doodle_p.drawRect(0, 0, self.width, self.height)
        self.draw_radius(doodle_p)
        if self.createMode == 'doodle_contour':
            doodle_pen = QPen(QColor(0, 0, 0), self.doodle_pen_size)
        else: 
            doodle_pen = QPen(QColor(255, 255, 255), self.doodle_pen_size)
        doodle_pen.setCapStyle(Qt.RoundCap)
        doodle_p.setPen(doodle_pen)
        doodle_p.setBrush(QColor(255, 160, 90))
        self.doodle_pixmap.save("a.png")
        return self.doodle_pixmap


    # # 显示不规则 pix
    # def mypix(self):
    #     #获得图片自身的遮罩
    #     back_mask = self.set_window(100,100,5)
    #     if back_mask is None:
    #         print("error back_mask")
    #         return False

    #     #将获得的图片的大小作为窗口的大小
    #     self.resize(back_mask.size())
    #     #增加一个遮罩
    #     self.setMask(back_mask)
    #     #print(self.pix.size())
    #     self.dragPosition = None
    #     return True

    # 重定义鼠标按下响应函数mousePressEvent(QMouseEvent)
    # 鼠标移动响应函数mouseMoveEvent(QMouseEvent)，使不规则窗体能响应鼠标事件，随意拖动。
    def mousePressEvent(self, event):
        #鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
        if event.button() == Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            # 当左键移动窗体修改偏移值
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 一般 paintEvent 在窗体首次绘制加载， 要重新加载paintEvent
    # 需要重新加载窗口使用 self.update() or  self.repaint()
    def paintEvent(self, event):
        # painter = QPainter(self)
        #在指定位置绘制图片
        # painter.drawPixmap(0, 0, self.width(), self.height(), QPixmap("./images/boy.jpeg"))
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ShapeWidget()
    form.show()
    app.exec_()