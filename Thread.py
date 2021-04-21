import threading
from pynput import keyboard
from pynput.keyboard import Listener, KeyCode, Key
from PIL import ImageGrab
import time


class ListenerForExitThread(threading.Thread):
    def __init__(self, _id, name, key_identifier='q'):
        super().__init__()
        self.daemon = True
        self._id = _id
        self.name = name
        self.key_identifier = key_identifier

    def on_press(self, key):
        if len(self.key_identifier) == 1:
            if key == KeyCode(char=self.key_identifier):
                return False
        elif key == Key(self.key_identifier):
            if key == KeyCode(char=self.key_identifier):
                return False

    def on_release(self, key):
        pass

    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


class DatabaseCreationThread(threading.Thread):
    def __init__(self, _id, name, coords, files=None, labels=None, run_instances=0, jump_instances=0):
        super().__init__()
        if labels is None:
            labels = []
        if files is None:
            files = []
        self.daemon = True
        self._id = _id
        self.name = name
        self.jump_instances = jump_instances
        self.run_instances = run_instances
        self.coords = coords
        self.files = files
        self.labels = labels
        self.is_set = False

    def get_data(self):
        return self.files, self.labels, self.jump_instances, self.run_instances

    def set(self):
        self.is_set = True

    def run(self):
        with keyboard.Events() as events:
            while True:
                if not self.is_set:
                    time.sleep(0.2)
                    event = events.get()
                    print('Received event {}'.format(event))
                    if event is None:
                        self.run_instances += 1
                        self.files.append(f"dataset\\dino_run_{self.run_instances}.png")
                        self.labels.append('Run')
                        img = ImageGrab.grab()
                        img = img.crop(self.coords)
                        img.save(f"dataset\\dino_run_{self.run_instances}.png")
                    else:
                        if event.key == Key.space:
                            self.jump_instances += 1
                            self.files.append(f"dataset\\dino_jump_{self.jump_instances}.png")
                            self.labels.append('Jump')
                            img = ImageGrab.grab()
                            img = img.crop(self.coords)
                            img.save(f"dataset\\dino_jump_{self.jump_instances}.png")
