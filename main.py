#s# 用于Python的PyQt5 GUI框架
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from Ui_mainWindow import Ui_MainWindow
import sys
import pyqtgraph as pg

# 继承QMainWindow创建一个主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.on_click)  # 连接按钮点击事件到处理函数

        self.mouseDatalabel = pg.LabelItem(justify='right')
        self.ui.graphicsView.addItem(self.mouseDatalabel)
        self.plot = self.ui.graphicsView.addPlot(title="Test", row=1, col=0)

        self.plot.showGrid(x=True, y=True)
        self.base_line = pg.PolyLineROI([[0, 0], [50, 0], [60, 10], [70, 30], [80, 50], [90, 100]], pen=pg.mkPen(color=(0, 255, 0), width=1), movable=False)
        self.base_line.checkPointMove = self.checkPointMove 

        self.plot.addItem(self.base_line)

        # 禁用横纵坐标自动调整
        self.plot.setAspectLocked()

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)

        self.plot.scene().sigMouseMoved.connect(self.mouseMoved)

        #设置横坐标范围
        self.plot.setXRange(0, 100, padding=0)
        self.plot.setYRange(-10, 110, padding=0)



    def mouseMoved(self, evt):
        pos = evt
        if self.plot.sceneBoundingRect().contains(pos):
            mouse_point = self.plot.vb.mapSceneToView(pos)
            # index = int(mouse_point.x())
            points = self.base_line.getState()['points']
            real_y = 0
            for index in range(len(points)):
                if(points[index][0] > mouse_point.x() and index!=0):
                    point_left = index - 1
                    diff_cur = points[index][0] -points[point_left][0]
                    diff_var = points[index][1] - points[point_left][1]
                    add_var = diff_var * (mouse_point.x()-points[point_left][0]) / diff_cur
                    real_y = points[point_left][1]+add_var
                    break
                if(index == len(points)):
                    real_y = points[index][1]        
            
            # if index > 0:
            self.mouseDatalabel.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: green'>y=%0.1f</span>, <span style='color: red'>y_line=%0.1f</span>" % (
                mouse_point.x(), mouse_point.y(), real_y))
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(real_y)


    def checkPointMove(self, handle, pos, modifiers):
        states = self.base_line.getState()
        points = states['points']
        if(len(points)>1):
            for index in range(1, len(points)):
                if(points[index][0] < points[index-1][0]):
                    points[index][0] = points[index-1][0]+1
                    states['points'] = points
                    self.base_line.setState(states)
                    return False
        return True



    # 点击按钮后的处理函数
    def on_click(self):
        states = self.base_line.getState()
        points = states['points']
        for it in points:
            print(it)


# 应用程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    window = MainWindow()  # 创建主窗口对象实例
    window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 进入应用程序主循环