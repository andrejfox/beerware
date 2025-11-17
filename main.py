import sys

from PySide6.QtCore import QSize, QThread, Signal
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from w1thermsensor import W1ThermSensor

# set the size of the window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1024

# set the size of the buttons
BUTTON_HEIGHT = 100
BUTTON_WIDTH = 300

# default target temp
TARGET_TEMP = 40
CURR_TEMP = 32

class TempReader(QThread):
    new_temp = Signal(float)

    def __init__(self, sensor):
        super().__init__()
        self.sensor = sensor
        self.running = True

    def run(self):
        while self.running:
            try:
                temp = self.sensor.get_temperature()
                self.new_temp.emit(temp)
            except:
                pass
            self.msleep(200)  # update 5 times per second

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeerWare")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon("./beer_pic.png"))
        self.setStyleSheet("""
                background-color: #2D2C2E;
                color: #FBBD0D;
                """)

        # List all sensors
        sensors = W1ThermSensor.get_available_sensors()

        print(f"Found {len(sensors)} sensors")
        for sensor in sensors:
            print(sensor.id)  # unique sensor ID

        self.sensor = W1ThermSensor()

        self.heating = QLabel(self)
        self.heating.setPixmap(QPixmap("heating_off.png"))
        self.heating.adjustSize()
        self.heating.move(self.width() - self.heating.width(), 0)

        self.temp_label = QLabel("Current temp: -- °C", self)
        self.temp_label.setFont(QFont("Roboto", 32))
        self.temp_label.adjustSize()
        self.temp_label.move(0, 50)  # position it somewhere

        self.sensor_thread = TempReader(self.sensor)
        self.sensor_thread.new_temp.connect(self.update_temp)
        self.sensor_thread.start()

        self.temp_target = QLabel(f'Target temp: {TARGET_TEMP:.1f} °C', self)
        self.temp_target.setFont(QFont("Roboto", 32))
        self.temp_target.adjustSize()

        b_plus = QPushButton("+", self)
        b_plus.setGeometry(0, WINDOW_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        b_plus.clicked.connect(self.b_plus_clicked)

        b_minus = QPushButton("-", self)
        b_minus.setGeometry(WINDOW_WIDTH - BUTTON_WIDTH, WINDOW_HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
        b_minus.clicked.connect(self.b_minus_clicked)

    def update_temp(self, current_temp):
        self.temp_label.setText(f"Current temp: {current_temp:.2f} °C")
        self.temp_label.adjustSize()

        if current_temp < TARGET_TEMP:
            self.heating_on()
        else:
            self.heating_off()

    def b_plus_clicked(self):
        global TARGET_TEMP
        TARGET_TEMP += 1
        self.temp_target.setText(f'Target temp: {TARGET_TEMP} °C')

    def b_minus_clicked(self):
        global TARGET_TEMP
        TARGET_TEMP -= 1
        self.temp_target.setText(f'Target temp: {TARGET_TEMP} °C')

    def heating_on(self):
        self.heating.setPixmap(QPixmap("heating_on.png"))
        self.heating.adjustSize()

    def heating_off(self):
        self.heating.setPixmap(QPixmap("heating_off.png"))
        self.heating.adjustSize()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
