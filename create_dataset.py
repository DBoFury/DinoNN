from PIL import ImageGrab
from Chrome import Chrome
from pynput import keyboard
import keyboard as kb
import pandas as pd
from config import DATASET_FILE_NAME

jump = 0
run = 0
files = []
labels = []


def main():
    global jump, run
    try:
        df = pd.read_csv(DATASET_FILE_NAME)
        jump = df[df['label'] == 'Jump'].count()['file']
        run = df[df['label'] == 'Run'].count()['file']
    except FileNotFoundError as filenotfoundex:
        print("Warning! No such directory was found.")

    print(jump, run)
    chrome = Chrome('https://trex-runner.com/', 'runner-canvas')

    def on_press(key):
        global files, labels, jump, run

        if key == keyboard.KeyCode(char='q'):
            chrome.quit()
            try:
                database = pd.read_csv(DATASET_FILE_NAME)
                database = database.append(pd.DataFrame({'file': files, 'label': labels}), ignore_index=True)
            except FileNotFoundError as filenotfoundex:
                print("Warning! No such directory was found.")
                database = pd.DataFrame({'file': files, 'label': labels})
            database.to_csv(DATASET_FILE_NAME, index=False)
            return False

        img = ImageGrab.grab()
        img = img.crop(chrome.coords)

        if key == keyboard.Key.space:
            jump += 1
            files.append(f"dataset\\dino_jump_{jump}.png")
            labels.append('Jump')
            img.save(f"dataset\\dino_jump_{jump}.png")
        if key == keyboard.KeyCode(char='e'):
            if not kb.is_pressed('space'):
                run += 1
                files.append(f"dataset\\dino_run_{run}.png")
                labels.append('Run')
                img.save(f"dataset\\dino_run_{run}.png")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


if __name__ == '__main__':
    main()
