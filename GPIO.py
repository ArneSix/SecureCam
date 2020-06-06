from gpiozero import Button
from multiprocessing import Process


class GPIO:
    def __init__(self):
        self._button_state: bool = False
        self._observers = []
        self.__button = Button(5)

        Process(target=self.run).start()

    @property
    def button_state(self):
        return self._button_state

    @button_state.setter
    def button_state(self, value):
        self._button_state = value
        for callback in self._observers:
            callback(self.button_state)

    def bind_to(self, callback):
        self._observers.append(callback)

    def run(self):
        while True:
            if self.__button.is_pressed:
                self.button_state = True



