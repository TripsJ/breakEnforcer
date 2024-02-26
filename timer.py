import time  # Keep track of time and sleep


class Timer:
    def __init__(self, name, target_time):
        self.name: str = name
        self.target_time = target_time

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def target_time(self):
        return self._target_time

    @target_time.setter
    def target_time(self, target_time):
        self._target_time = target_time

    def set_timer(self, inputstr: str):
        """set the timer from a given input"""
        inputstr = inputstr.lower()
        if "h" in inputstr:
            splitchar = "h"
        elif ":" in inputstr:
            splitchar = ":"
        else:
            raise ValueError("Time Format must be HH:MM of HHhMM")

        h, m = inputstr.split(splitchar)
        # check for valid integers
        hours: int = int(h)
        minutes: int = int(m)

        self.target_time = f"{hours}:{minutes}"

    def run_timer(self) -> bool:
        """Run the timer"""
        current_time: str = time.strftime("%H:%M")
        while current_time != self.target_time:
            time.sleep(1)
            current_time: str = time.strftime("%H:%M")
            print(current_time)
        return True
