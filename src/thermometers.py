from typing import Optional, Dict

from w1thermsensor import W1ThermSensor
import threading
import time

class Thermometers:
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
        last_rescan = time.time()

        while self._running:
            for sensor in list(self.sensors):
                try:
                    self.temperatures[sensor.id] = sensor.get_temperature()
                except Exception as e:
                    print(f"Error reading sensor {sensor.id}: {e}")
                    self.temperatures[sensor.id] = None

            if time.time() - last_rescan >= 5:
                self._rescan_sensors()
                last_rescan = time.time()

            print(self.temperatures)
            time.sleep(self.update_interval)

    def _rescan_sensors(self):
        found = W1ThermSensor.get_available_sensors()
        found_ids = {s.id for s in found}
        current_ids = {s.id for s in self.sensors}

        for sensor in found:
            if sensor.id not in current_ids:
                print(f"[+] New sensor detected: {sensor.id}")
                self.sensors.append(sensor)
                self.temperatures[sensor.id] = None

        removed_ids = current_ids - found_ids
        if removed_ids:
            for sid in removed_ids:
                print(f"[-] Sensor removed: {sid}")
                self.temperatures.pop(sid, None)
            self.sensors = [s for s in self.sensors if s.id in found_ids]

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