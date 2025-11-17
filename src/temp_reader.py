from PySide6.QtCore import QThread, Signal

class TempReader(QThread):
    cur_temp = Signal(float)

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
            self.msleep(1000)

    def stop(self):
        self.running = False
        self.wait()
