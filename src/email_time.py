class email_time:

    def __init__(self, time):
        self.time = time
        self.has_passed_var = False

    # has_passed(): String
    def has_passed(self):
        return self.has_passed_var

    # set_passed(state: boolean): void
    def set_passed(self, state):
        self.has_passed_var = state

    # get_time(): String
    def get_time(self):
        return self.time

