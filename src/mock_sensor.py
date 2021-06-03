import random
import math
import logger

class MockSensor:

    def __init__ (self):
        self.base = random.randrange(25, 75)

    def gen_new_percent(self):
        """This updates the current level of the fake Well Manager
        """
        if self.base >= 95:
            self.base -= 5
        if self.base <= 5:
            self.base += 5
        num = random.randint(-1030, 1030)
        num = ((0.001 * num) ** 100) + (random.randint(0, 2) / 15)
        negop = random.randint(0, 1)
        if(negop == 0):
            negop = -1
        self.base += num * negop

    def get_percent(self):
        """Return the new level of he fake well manager

        Returns:
            Double: The percentage level of the fake Well Manager(0 - 100)
        """
        self.gen_new_percent()
        return self.base

    def cleanup(self):
        logger.log_event("Mock sensor is cleaning up...")
