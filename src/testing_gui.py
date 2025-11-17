import threading
import time

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QLabel, QPushButton, QMainWindow, QApplication

DUMMY_TEMP = 23

class MainWindow(QMainWindow):
    def __init__(self, w_height, w_width, temp_target):
        super().__init__()

        self.temp_target = temp_target

        self.setWindowTitle("BeerWare")
        self.setFixedSize(QSize(w_width, w_height))
        self.setWindowIcon(QIcon("../pics/beer_pic.png"))
        self.setStyleSheet("""
            background-color: #2D2C2E;
            color: #FBBD0D;
        """)

        self.heating_label = QLabel(self)
        self.heating_label.setPixmap(QPixmap("./pics/heating_off.png"))
        self.heating_label.adjustSize()
        self.heating_label.move(self.width() - self.heating_label.width(), 0)

        self.temp_label = QLabel("Current temp: -- °C", self)
        self.temp_label.setFont(QFont("Roboto", 32))
        self.temp_label.adjustSize()
        self.temp_label.move(0, 50)  # position it somewhere

        self.temp_target_label = QLabel(f'Target temp: {self.temp_target:.1f} °C', self)
        self.temp_target_label.setFont(QFont("Roboto", 32))
        self.temp_target_label.adjustSize()

        b_plus = QPushButton("+", self)
        b_plus.setGeometry(0, self.height() - 100, 200, 100)
        b_plus.clicked.connect(self.b_plus_clicked)

        b_minus = QPushButton("-", self)
        b_minus.setGeometry(self.width() - 200, self.height() - 100, 200, 100)
        b_minus.clicked.connect(self.b_minus_clicked)

        exit_button = QPushButton("EXIT", self)
        exit_button.setStyleSheet("background-color: red; color: white; font-size: 32px;")
        exit_button.setGeometry(
            (self.width() // 2) - 150,  # center X
            self.height() - 100 - 120,  # slightly above bottom
            300, 100  # size
        )
        exit_button.clicked.connect(self.exit_app)

        thread = threading.Thread(target=self.sensor_simulator, daemon=True)
        thread.start()

    def sensor_simulator(self):
        global DUMMY_TEMP
        while True:
            self.update_temp(DUMMY_TEMP)

            if self.temp_target > DUMMY_TEMP:
                DUMMY_TEMP += 1
                self.heating_on()
            elif self.temp_target < DUMMY_TEMP:
                DUMMY_TEMP -= 1
                self.heating_off()
            else:
                self.heating_off()

            time.sleep(1)


    def exit_app(self):
        print("Exiting...")
        QApplication.quit()


    def update_temp(self, current_temp):
        self.temp_label.setText(f"Current temp: {current_temp:.2f} °C")
        self.temp_label.adjustSize()

        if current_temp < self.temp_target:
            self.heating_on()
        else:
            self.heating_off()

    def b_plus_clicked(self):
        self.temp_target += 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target} °C')

    def b_minus_clicked(self):
        self.temp_target -= 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target} °C')

    def heating_on(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_on.png"))
        self.heating_label.adjustSize()

    def heating_off(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_off.png"))
        self.heating_label.adjustSize()
