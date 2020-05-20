from Camera import Camera
from GPIO import GPIO


class App:
    def __init__(self, gpio: GPIO):
        self.button_state: bool = False
        self.gpio: GPIO = gpio
        self.camera: Camera = Camera(video_device=0)

        self.gpio.bind_to(self.update_button_state)

    def update_button_state(self, button_state):
        self.button_state = button_state
        self.camera.start()
