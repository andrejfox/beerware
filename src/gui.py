from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QLabel, QPushButton, QMainWindow, QApplication

from src.heating import Heating
from src.thermometer import Thermometers


class MainWindow(QMainWindow):
    def __init__(self, w_height, w_width, temp_target):
        super().__init__()
        self.temp_target = temp_target

        self.heating_system = Heating(18, 10, 3, 0.3)
        self.thermometer_system = Thermometers(1.0)

        self.heating_system.start()
        self.thermometer_system.start()

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
        self.temp_label.move(0, 50)

        self.temp_target_label = QLabel(f'Target temp: {self.temp_target:.2f} °C', self)
        self.temp_target_label.setFont(QFont("Roboto", 32))
        self.temp_target_label.adjustSize()

        b_plus = QPushButton("+", self)
        b_plus.setGeometry(0, self.height() - 100, 200, 100)
        b_plus.clicked.connect(self.b_plus_clicked)

        b_minus = QPushButton("-", self)
        b_minus.setGeometry(self.width() - 200, self.height() - 100, 200, 100)
        b_minus.clicked.connect(self.b_minus_clicked)

        # --- EXIT BUTTON ---
        exit_button = QPushButton("EXIT", self)
        exit_button.setStyleSheet("background-color: red; color: white; font-size: 32px;")
        exit_button.setGeometry(
            (self.width() // 2) - 150,  # center X
            self.height() - 100 - 120,  # slightly above bottom
            300, 100  # size
        )
        exit_button.clicked.connect(self.exit_app)

        self.showFullScreen()

    def exit_app(self):
        print("Exiting...")
        self.heating_system.stop()
        self.thermometer_system.stop()

        QApplication.quit()


    def update_temp(self, cur_temp):
        self.temp_label.setText(f"Current temp: {cur_temp:.2f} °C")
        self.temp_label.adjustSize()

        if cur_temp < self.temp_target:
            self.heating_on()
        else:
            self.heating_off()

    def b_plus_clicked(self):
        self.temp_target += 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target:.2f} °C')

    def b_minus_clicked(self):
        self.temp_target -= 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target:.2f} °C')

    def heating_on(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_on.png"))
        self.heating_label.adjustSize()
        self.heating_relay.on()

    def heating_off(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_off.png"))
        self.heating_label.adjustSize()
        self.heating_relay.off()