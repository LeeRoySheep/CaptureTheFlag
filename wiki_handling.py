from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
