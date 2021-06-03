# Module imports
#################################3import RPi.GPIO as GPIO
import time

# My imports
import logger

class Sensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.TRIG = 23
        self.ECHO = 24
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.setwarnings(False)

    def get_distance(self):
        """Gets the distance of water to the sensor in inches
        Returns:
            [double]: percentage reading
                        or
                        -1: if sensor hangs
        """
        
        SPEED_OF_SOUND =  1125.0 * 12.0 # in inches/second
        # Send trigger signal
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        timer_start= time.time()
        pulseStart = time.time()
        # Measure the ECHO high time
        while GPIO.input(self.ECHO) == 0 :
            pulseStart = time.time()
            if(pulseStart - timer_start > 1):
                return -1

        while GPIO.input(self.ECHO) == 1 :
            pulseEnd = time.time()
            if(pulseEnd - pulseStart > 1):
                return -1

        # get the delta
        pulseDuration = pulseEnd - pulseStart

        # distance traveled to water level
        distance = pulseDuration * (SPEED_OF_SOUND / 2)
        if(distance < 0):
            distance = 0
        #GPIO.cleanup()
        return distance

    def get_percent(self):
        """Return the current level of the Well Manager as a percent

        Returns:
            double: Water level percentage (0- 100)
        """
        dist = self.get_distance()
        sensorDist = 3.5 # distance from sensor to max fill line
        # top to bottom = 55.5 inches
        maxInches = 52.0 # inches from 0% water to 100% water
        percent = ((maxInches - dist + sensorDist)/maxInches) * 100
        return percent

    def cleanup(self):
        """Cleans up the GPIO pins before stopping the program
        """
        logger.log_event("Cleaning up GPIO pins...")
        GPIO.cleanup()
