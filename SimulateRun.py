from Chrome import Chrome
from PIL import ImageGrab
import keyboard
from utils import *
from Thread import ListenerForExitThread


def main(acceleration=False):
    chrome = Chrome('https://trex-runner.com/', 'runner-canvas', acceleration)
    try:
        nn = load_nn()
    except FileNotFoundError as filenotfoundex:
        print(filenotfoundex)
        return

    thread = ListenerForExitThread(1, "Listen for 'q'")
    thread.start()

    while True:
        img = ImageGrab.grab()
        img = img.crop(chrome.coords)

        if nn.predict(convert_image(image=img)).argmax() == 0:
            jump = True
        else:
            jump = False

        if jump:
            keyboard.press('space')
        else:
            keyboard.release('space')

        try:
            if chrome.get_crashed():
                chrome.restart()
        except:
            break

        if not thread.is_alive():
            chrome.quit()
            break


if __name__ == '__main__':
    main(acceleration=False)
