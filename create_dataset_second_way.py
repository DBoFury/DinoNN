from Chrome import Chrome
import pandas as pd
from config import DATASET_FILE_NAME
from Thread import ListenerForExitThread, DatabaseCreationThread


def main():
    try:
        df = pd.read_csv(DATASET_FILE_NAME)
        jump = df[df['label'] == 'Jump'].count()['file']
        run = df[df['label'] == 'Run'].count()['file']
    except FileNotFoundError as filenotfoundex:
        jump, run = 0, 0
        print("Warning! No such directory was found.")

    print(jump, run)
    chrome = Chrome('https://trex-runner.com/', 'runner-canvas')
    coords = chrome.coords

    listener_thread = ListenerForExitThread(1, "Listener for 'q'")
    listener_thread.start()

    dataset_creation_thread = DatabaseCreationThread(2, "Thread for creation dataset", coords,
                                                     jump_instances=jump, run_instances=run)
    dataset_creation_thread.start()

    while True:
        if chrome.get_crashed():
            chrome.restart()

        if not listener_thread.is_alive():
            files, labels, jump, run = dataset_creation_thread.get_data()
            dataset_creation_thread.set()
            chrome.quit()
            try:
                df = pd.read_csv(DATASET_FILE_NAME)
                df = df.append(pd.DataFrame({'file': files, 'label': labels}), ignore_index=True)
            except FileNotFoundError as filenotfoundex:
                print("Warning! No such directory was found.", flush=True)
                df = pd.DataFrame({'file': files, 'label': labels})
            df.to_csv(DATASET_FILE_NAME, index=False)
            break


if __name__ == '__main__':
    main()
