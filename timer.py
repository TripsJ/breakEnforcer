import time
from tkinter import *
from tkinter.ttk import *


class Timer:
    def __init__(self):
        self.duration = ""
        self.countdown = -1
        self.root = Tk()
        self.lable = Label(self.root, font=("calibri", 30))

    def __str__(self):
        return f"This Timer is set to run for {self.duration} and has {self.countdown} seconds left"

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration.lower()

    @property
    def countdown(self):
        return self._countdown

    @countdown.setter
    def countdown(self, countdown):
        self._countdown = countdown

    def set_timer(self):
        if "h" in self.duration:
            splitchar = h
        elif ":" in self.duration:
            splitchar = ":"

        sh, sm = self.duration.split(splitchar)
        h = int(sh)
        m = int(sm) + (h * 60)
        self.countdown = m * 60

    def run(self) -> bool:
        """Run the timer"""
        if self.countdown < 0:
            print("please set timer first")
        else:
            self.lable.pack(anchor="center")
            self.updateDisplay()
            self.root.mainloop()
            return True

    def updateDisplay(self):
        while self._countdown > 0:
            self.lable.config(text=self.countdown)
            self.countdown -= 1
            self.lable.after(1000, self.updateDisplay)
        return True
