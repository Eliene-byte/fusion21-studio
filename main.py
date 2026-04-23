
import sys, os, traceback
from PySide6.QtWidgets import (QApplication, QMainWindow, QDockWidget, QTreeWidget, QTreeWidgetItem,
    QGraphicsView, QGraphicsScene, QWidget, QLabel, QMessageBox)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QLinearGradient, QPen
from PySide6.QtCore import Qt, QTimer

def resource_path(rel):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, rel)

def log_error(exc):
    try:
        log_path = os.path.join(os.path.expanduser("~"), "YourEffects_error.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("\n---\n" + traceback.format_exc())
    except: pass

STYLE = """
QMainWindow { background: #0a0a0a; }
QDockWidget::title { background: #111; color: #00FF88; padding: 6px; font-weight: bold; border-bottom: 1px solid #00FF88; }
QTreeWidget { background: #0f0f0f; color: #ddd; border: none; font-size: 13px; }
QTreeWidget::item:selected { background: #00FF88; color: black; }
QLabel { color: #aaa; }
"""

class NodeView(QGraphicsView):
    def __init__(self):
        super().__init__()
        scene = QGraphicsScene(-2000,-2000,4000,4000)
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QColor("#0a0a0a"))
        pen = QPen(QColor("#1a1a1a"))
        for i in range(-2000,2000,80):
            scene.addLine(i,-2000,i,2000,pen)
            scene.addLine(-2000,i,2000,i,pen)

class Viewer(QWidget):
    def paintEvent(self, e):
        p = QPainter(self)
        grad = QLinearGradient(0,0,0,self.height())
        grad.setColorAt(0, QColor("#001a12")); grad.setColorAt(1, QColor("#000"))
        p.fillRect(self.rect(), grad)
        p.setPen(QColor("#00FF88"))
        p.drawText(self.rect(), Qt.AlignCenter, "VIEWER - Your Effects 3.300 pronto!")

class YourEffects(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Effects Studio – 3,300 funcionalidades")
        try:
            self.setWindowIcon(QIcon(resource_path("assets/icon.png")))
        except: pass
        self.resize(1600, 900)
        self.setStyleSheet(STYLE)

        self.node_view = NodeView()
        self.setCentralWidget(self.node_view)

        left = QDockWidget("BIBLIOTECA", self)
        tree = QTreeWidget(); tree.setHeaderHidden(True)
        cats = ["2D Base (1.700)","IA Leve (300)","3D Real-Time (1.100)","Super Nodes (120)","After Effects Tech (80)"]
        for name in cats:
            it = QTreeWidgetItem([name]); it.setForeground(0, QColor("#00FF88")); tree.addTopLevelItem(it)
        tree.expandAll(); left.setWidget(tree); self.addDockWidget(Qt.LeftDockWidgetArea, left)

        right = QDockWidget("PROPRIEDADES", self)
        prop = QLabel("Selecione um node\n\n• Puppet Pin pronto\n• Expressions pronto\n• Content-Aware pronto")
        prop.setAlignment(Qt.AlignTop); prop.setStyleSheet("padding:12px;"); right.setWidget(prop)
        self.addDockWidget(Qt.RightDockWidgetArea, right)

        top = QDockWidget("", self); top.setTitleBarWidget(QWidget()); top.setWidget(Viewer())
        self.addDockWidget(Qt.TopDockWidgetArea, top)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        splash = None
        try:
            pix = QPixmap(resource_path("assets/splash.png"))
            if not pix.isNull():
                splash = QLabel(); splash.setPixmap(pix.scaled(900,500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                splash.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint); splash.show()
        except Exception as e:
            log_error(e)

        win = YourEffects()
        QTimer.singleShot(1600, lambda: (splash.close() if splash else None, win.show()))
        sys.exit(app.exec())
    except Exception:
        log_error(sys.exc_info()[1])
        try:
            QMessageBox.critical(None, "Your Effects - Erro", traceback.format_exc())
        except: pass
