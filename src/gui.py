from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QLabel, QPushButton, QMainWindow, QApplication
from w1thermsensor import W1ThermSensor

from temp_reader import TempReader


class MainWindow(QMainWindow):
    def __init__(self, w_height, w_width, temp_target):
        super().__init__()

        self.temp_target_label = temp_target

        self.setWindowTitle("BeerWare")
        self.setFixedSize(QSize(w_width, w_height))
        self.setWindowIcon(QIcon("../pics/beer_pic.png"))
        self.setStyleSheet("""
            background-color: #2D2C2E;
            color: #FBBD0D;
        """)
        self.showFullScreen()

        sensors = W1ThermSensor.get_available_sensors()

        print(f"Found {len(sensors)} sensors")
        for sensor in sensors:
            print(sensor.id)

        self.sensor = W1ThermSensor()

        self.heating_label = QLabel(self)
        self.heating_label.setPixmap(QPixmap("./pics/heating_off.png"))
        self.heating_label.adjustSize()
        self.heating_label.move(self.width() - self.heating_label.width(), 0)

        self.temp_label = QLabel("Current temp: -- °C", self)
        self.temp_label.setFont(QFont("Roboto", 32))
        self.temp_label.adjustSize()
        self.temp_label.move(0, 50)  # position it somewhere

        self.sensor_thread = TempReader(self.sensor)
        self.sensor_thread.cur_temp.connect(self.update_temp)
        self.sensor_thread.start()

        self.temp_target_label = QLabel(f'Target temp: {self.temp_target_label:.1f} °C', self)
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

    def exit_app(self):
        print("Exiting...")

        # stop thread safely
        if self.sensor_thread.isRunning():
            self.sensor_thread.running = False
            self.sensor_thread.quit()
            self.sensor_thread.wait()

        QApplication.quit()


    def update_temp(self, cur_temp):
        self.temp_label.setText(f"Current temp: {cur_temp:.2f} °C")
        self.temp_label.adjustSize()

        if cur_temp < self.temp_target_label:
            self.heating_on()
        else:
            self.heating_off()

    def b_plus_clicked(self):
        self.temp_target_label += 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target_label} °C')

    def b_minus_clicked(self):
        self.temp_target_label -= 1
        self.temp_target_label.setText(f'Target temp: {self.temp_target_label} °C')

    def heating_on(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_on.png"))
        self.heating_label.adjustSize()

    def heating_off(self):
        self.heating_label.setPixmap(QPixmap("./pics/heating_off.png"))
        self.heating_label.adjustSize()