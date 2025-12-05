from typing import Optional, Dict

from w1thermsensor import W1ThermSensor
import threading
import time

class Thermometers:
    offsets = {
        'db5a7d0a6461': 5.93,
        '8490710a6461': -3.5
    }

    def __init__(self, update_interval=1.0):
        self.sensors = W1ThermSensor.get_available_sensors()
        print(f"Found {len(self.sensors)} sensors")
        for sensor in self.sensors:
            print(sensor.id)

        # Create a dictionary: sensor_id -> temperature
        self.temperatures: Dict[str, Optional[float]] = {sensor.id: None for sensor in self.sensors}

        self.update_interval = update_interval
        self._running = False
        self._thread = None

    def _update_loop(self):
        while self._running:
            for sensor in list(self.sensors):
                try:
                    self.temperatures[sensor.id] = sensor.get_temperature() + self.offsets[sensor.id]
                except Exception as e:
                    print(f"Error reading sensor {sensor.id}: {e}")
                    self.temperatures[sensor.id] = None

            print(self.temperatures)
            time.sleep(self.update_interval)

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._update_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def get_temperature(self, sensor_id):
        return self.temperatures.get(sensor_id, None)