import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeerWare")
        self.setFixedSize(QSize(1024, 600))
        self.setWindowIcon(QIcon("./beer_pic.png"))

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        self.setCentralWidget(button)

    def the_button_was_clicked(self):
            print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    main()