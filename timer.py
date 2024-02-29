import time
from datetime import timedelta


class Timer:
    def __init__(self, target_time=time.strftime("%H:%M")):
        self.target_time = target_time

    @property
    def target_time(self):
        return self._target_time

    @target_time.setter
    def target_time(self, target_time):
        target_time = target_time.lower()
        if "h" in target_time:
            splitchar = "h"
        elif ":" in target_time:
            splitchar = ":"
        else:
            raise ValueError("Time Format must be HH:MM of HHhMM")

        h, m = target_time.split(splitchar)
        # check for valid integers
        hours: int = int(h)
        minutes: int = int(m)
        timestring = f"{hours:02d}:{minutes:02d}"

        self._target_time = timestring

    # def set_timer(self):
    #    """set the timer from a given input"""
    #   inputstr = input()

    def run(self) -> bool:
        """Run the timer"""
        current_time: str = time.strftime("%H:%M")
        while current_time != self.target_time:
            time.sleep(1)
            current_time: str = time.strftime("%H:%M")
            print(current_time)
        return True
