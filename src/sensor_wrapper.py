import sensor
import mock_sensor

class GeneralSensor:

    # __init__ (self: GeneralSensor, mock: boolean): void
    def __init__ (self, mock):
        if(mock):
            self.sensor = mock_sensor.MockSensor()
        else:
            self.sensor = sensor.Sensor()

    def get_percent(self):
        return self.sensor.get_percent()

    def cleanup(self):
        return self.sensor.cleanup()
