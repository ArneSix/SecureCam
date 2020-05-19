class GPIO:
    def __init__(self):
        self._button_state: bool = False
        self._observers = []

    @property
    def button_state(self):
        return self._button_state

    @button_state.setter
    def button_state(self, value):
        self._button_state = value
        for callback in self._observers:
            print(f"state changed")
            callback(self.button_state)

    def bind_to(self, callback):
        self._observers.append(callback)
