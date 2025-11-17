import sys

from PySide6.QtCore import QSize, QThread, Signal
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from w1thermsensor import W1ThermSensor


WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1024

DEFAULT_TARGET_TEMP = 40

class TempReader(QThread):
    cur_temp = Signal(float)  # signal emits new temperature

    def __init__(self, sensor):
        super().__init__()
        self.sensor = sensor
        self.running = True

    def run(self):
        while self.running:
            try:
                temperature = self.sensor.get_temperature()
                self.cur_temp.emit(temperature)
            except Exception as e:
                print(f"Sensor error: {e}")
            self.msleep(100)

    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeerWare")
        self.setFixedSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.setWindowIcon(QIcon("pics/beer_pic.png"))
        self.setStyleSheet("""
            background-color: #2D2C2E;
            color: #FBBD0D;
        """)

        sensors = W1ThermSensor.get_available_sensors()

        print(f"Found {len(sensors)} sensors")
        for sensor in sensors:
            print(sensor.id)

        self.sensor = W1ThermSensor()

        self.heating = QLabel(self)
        self.heating.setPixmap(QPixmap("pics/heating_off.png"))
        self.heating.adjustSize()
        self.heating.move(self.width() - self.heating.width(), 0)

        self.temp_label = QLabel("Current temp: -- °C", self)
        self.temp_label.setFont(QFont("Roboto", 32))
        self.temp_label.adjustSize()
        self.temp_label.move(0, 50)  # position it somewhere

        self.sensor_thread = TempReader(self.sensor)
        self.sensor_thread.temp.connect(self.update_temp)
        self.sensor_thread.start()

        self.temp_target = QLabel(f'Target temp: {DEFAULT_TARGET_TEMP:.1f} °C', self)
        self.temp_target.setFont(QFont("Roboto", 32))
        self.temp_target.adjustSize()

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


    def update_temp(self, current_temp):
        self.temp_label.setText(f"Current temp: {current_temp:.2f} °C")
        self.temp_label.adjustSize()

        if current_temp < DEFAULT_TARGET_TEMP:
            self.heating_on()
        else:
            self.heating_off()

    def b_plus_clicked(self):
        global DEFAULT_TARGET_TEMP
        DEFAULT_TARGET_TEMP += 1
        self.temp_target.setText(f'Target temp: {DEFAULT_TARGET_TEMP} °C')

    def b_minus_clicked(self):
        global DEFAULT_TARGET_TEMP
        DEFAULT_TARGET_TEMP -= 1
        self.temp_target.setText(f'Target temp: {DEFAULT_TARGET_TEMP} °C')

    def heating_on(self):
        self.heating.setPixmap(QPixmap("pics/heating_on.png"))
        self.heating.adjustSize()

    def heating_off(self):
        self.heating.setPixmap(QPixmap("pics/heating_off.png"))
        self.heating.adjustSize()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
