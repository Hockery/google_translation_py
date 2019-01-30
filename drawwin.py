
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QCursor, QBitmap, QIcon
from PyQt5.QtCore import Qt, QPoint
from qtpy.QtGui import QPen, QColor
from HandleJs import Py4Js    
import re

import main 
#Python控制鼠标和键盘-PyAutoGUI

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
        self.js = Py4Js()   

        #创建多行文本框
        self.textEdit1=QTextEdit()
        self.textEdit2=QLabel()
        self.textEdit2.setWordWrap(True)
        #创建两个按钮
        self.btnPress1=QPushButton('清空')
        self.btnPress2=QPushButton('翻译')

        #实例化垂直布局
        layout=QVBoxLayout()
        #相关控件添加到垂直布局中
        layout.addWidget(self.textEdit1)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btnPress1)
        btn_layout.addWidget(self.btnPress2)
        layout.addLayout(btn_layout)
        layout.addWidget(self.textEdit2)

        #设置布局
        self.setLayout(layout)
        #将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress1.clicked.connect(self.btnPress1_clicked)
        self.btnPress2.clicked.connect(self.btnPress2_clicked)

    def deal_control_char(self, s):
        temp=re.sub('[\x00-\x09|\x0b-\x0c|\x0e-\x1f]','',s)
        return temp

    def btnPress1_clicked(self):
        #以文本的形式输出到多行文本框
        self.textEdit2.setText('')
        self.textEdit1.setPlainText('')

    def btnPress2_clicked(self):
        #以Html的格式输出多行文本框，字体红色，字号6号
        text = self.deal_control_char(self.textEdit1.toPlainText()).strip()
             
        if text == '':
            return
        print(text)
        # return 
        tk = self.js.getTk(text)    
        result=main.translate(text,tk) 
        print ("result: ", result)
        end = result.find("\",")    
        if end > 4:    
            print(result[4:end]) 
        self.textEdit2.setText(result[4:end])

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
        
        doodle_p.setBrush(QColor(0, 0, 0))
        doodle_p.drawRect(0, 0, self.width, self.height)
        self.draw_radius(doodle_p)

        doodle_p.setBrush(QColor(255, 160, 90))
        self.doodle_pixmap.save("a.png")
        return self.doodle_pixmap

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