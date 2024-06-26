import sys

sys.dont_write_bytecode = True

import os
import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib import *

scene = Scene(sys.argv[1]) if len(sys.argv) > 1 else Scene()

class PaintWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super(PaintWidget, self).__init__(parent=parent)
        self.width = width
        self.height = height

        self.imgBuffer = QImage(self.width, self.height, QImage.Format_ARGB32_Premultiplied)
        self.imgBuffer.fill(QColor(0, 0, 0))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawImage(0, 0, self.imgBuffer)

    def sizeHint(self):
        return QSize(self.width, self.height)


class PyTraceMainWindow(QMainWindow):
    def __init__(self, qApp, width, height):
        super(PyTraceMainWindow, self).__init__()

        self.qApp = qApp
        self.width = width
        self.height = height
        self.gfxScene = QGraphicsScene()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"PyTrace")
        self.resize(self.width + 25, self.height + 25)
        self.setWindowTitle("CENG488 PyTrace")
        self.setStyleSheet("background-color:black;")
        self.setAutoFillBackground(True)

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName(u"CentralWidget")

        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.gfxScene.setItemIndexMethod(QGraphicsScene.NoIndex)

        self.paintWidget = PaintWidget(self.width, self.height)
        self.paintWidget.setGeometry(QRect(0, 0, self.width, self.height))
        self.paintWidgetItem = self.gfxScene.addWidget(self.paintWidget)
        self.paintWidgetItem.setZValue(0)

        self.gfxView = QGraphicsView(self.centralWidget)
        self.gfxView.setObjectName(u"GraphicsView")

        self.gfxView.setScene(self.gfxScene)
        self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

        self.horizontalLayout.addWidget(self.gfxView)

        self.setCentralWidget(self.centralWidget)

        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName(u"StatusBar")
        self.statusBar.setStyleSheet("background-color:gray;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready...")

    def timerBuffer(self):
        start_time = time.time()
        num_threads = scene.renderSettings.get("num_threads") if scene.renderSettings != None else os.cpu_count()
        num_threads = min(os.cpu_count(), num_threads)
        num_spheres = len(scene.spheres) if scene.spheres != None else 0
        num_tris = len(scene.triangles) if scene.spheres != None else 0
        if scene.spheres != None:
            self.rayTracer = RayTracer(self.width, self.height, scene, num_threads)
            img_data = self.rayTracer.rayTrace()
            self.updateBufferImage(img_data)

        end_time = time.time()
        runtime = end_time - start_time
        if scene.spheres != None:
            if num_spheres == 0:
                self.statusBar.showMessage("Render Finished in {}m {:.0f}s!, number of threads: {}, number of triangles: {}".format(int(runtime//60), runtime % 60, num_threads, num_tris))
            elif num_tris == 0:
                self.statusBar.showMessage("Render Finished in {}m {:.0f}s!, number of threads: {}, number of spheres: {}".format(int(runtime//60), runtime % 60, num_threads, num_spheres))
            else:
                self.statusBar.showMessage("Render Finished in {}m {:.0f}s!, number of threads: {}, number of spheres: {}, number of triangles: {}".format(int(runtime//60), runtime % 60, num_threads, num_spheres, num_tris))
        else:
            self.statusBar.showMessage("JSON file is not valid")
        mainTimer.stop()

    def updateBufferImage(self, img_data):
        img = QImage(img_data, self.width, self.height, QImage.Format_RGB888)
        self.paintWidget.imgBuffer = img.copy()
        self.paintWidget.update()




if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    qApp.setOrganizationName("CENG488")
    qApp.setOrganizationDomain("cavevfx.com")
    qApp.setApplicationName("PyTrace")

    if scene.renderSettings != None:
        width = scene.renderSettings.get("xres")
        height = scene.renderSettings.get("yres")
    else: 
        width = 512
        height = 512

    mainWindow = PyTraceMainWindow(qApp, width, height)
    mainWindow.setupUi()
    mainWindow.show()

    mainTimer = QTimer()
    mainTimer.timeout.connect(mainWindow.timerBuffer)
    mainTimer.start(200)

    sys.exit(qApp.exec_())
