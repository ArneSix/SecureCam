from Camera import Camera
from GPIO import GPIO
from Detected import Detected


class App:
    def __init__(self):
        self.button_state: bool = False
        self.gpio: GPIO = GPIO()
        self.gpio.bind_to(self.update_button_state)

        self.camera: Camera = Camera(video_device=0)

    def update_button_state(self, button_state):
        self.button_state = button_state

        self.validate()

    def validate(self):
        if self.button_state:
            capture_result = self.camera.detect()

            if capture_result == Detected.VALID:
                print('yeeey I know you')
            elif capture_result == Detected.INVALID:
                print('I dunno man, seems fishy')
            else:
                print('you expected a result, BUT IT WAS ME....DIO')

