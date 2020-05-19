from App import App
from GPIO import GPIO

if __name__ == '__main__':
    gpio = GPIO()
    app = App(gpio)

    print(app.button_state)

    gpio.button_state = True

    print(app.button_state)
