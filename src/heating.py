from gpiozero import OutputDevice
import threading
import time

class Heating:
    heater0 = False
    heater1 = False
    heater0_relay = None
    heater1_relay = None

    def __init__(self, heater0_pin, heater1_pin, update_interval=20.0, buffer_interval=0.3):
        self.heater0_relay = OutputDevice(heater0_pin, active_high=True, initial_value=False)
        self.heater1_relay = OutputDevice(heater1_pin, active_high=True, initial_value=False)
        self.swap_interval = update_interval
        self.swap_buffer_interval = buffer_interval
        self._running = False
        self._thread = None

    def _run(self):
        toggle = False
        try:
            while self._running:
                if self.heater0 and self.heater1:
                    # Safety off before toggling
                    self.heater0_relay.off()
                    self.heater1_relay.off()
                    time.sleep(self.swap_buffer_interval)

                    toggle = not toggle
                    if toggle:
                        self.heater0_relay.on()
                        self.heater1_relay.off()
                    else:
                        self.heater0_relay.off()
                        self.heater1_relay.on()

                    time.sleep(self.swap_interval)
                else:
                    # Single heater or none
                    if not self.heater0:
                        self.heater0_relay.off()

                    if not self.heater1:
                        self.heater1_relay.off()

                    if self.heater0:
                        self.heater0_relay.on()

                    if self.heater1:
                        self.heater1_relay.on()

                    time.sleep(self.swap_interval)
        finally:
            self.heater0_relay.off()
            self.heater1_relay.off()

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
        self.heater0_relay.off()
        self.heater1_relay.off()