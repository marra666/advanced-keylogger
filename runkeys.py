import pyautogui
import time
from datetime import datetime
from pynput.keyboard import Key, Controller, Listener
import threading

key_mapping = {
    'Key.space': Key.space,
    'Key.shift': Key.shift,
    'Key.ctrl': Key.ctrl,
    'Key.alt': Key.alt,
    'Key.tab': Key.tab,
    'Key.enter': Key.enter,
    'Key.esc': Key.esc,
    'Key.space': Key.space,
}

keyboard = Controller()

def main_loop():
    global running
    global typing_enabled

    while running:
        try:
            txt = open('keyboard_log.txt', 'r')

            for line in txt:
                if not typing_enabled:
                    break

                line = line.strip()
                parts = line.split(': ')

                if len(parts) == 2:
                    time_str = parts[0]
                    key_name = parts[1]

                    time_stamp = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')

                    sleep_time = (time_stamp - datetime.now()).total_seconds()

                    if sleep_time > 0:
                        time.sleep(sleep_time)

                    key_to_press = key_mapping.get(key_name, key_name)

                    if isinstance(key_to_press, Key):
                        keyboard.press(key_to_press)
                        keyboard.release(key_to_press)
                    else:
                        pyautogui.press(key_to_press)
                else:
                    print(f"Ignoring line with unexpected format: {line}")

            txt.close()
        except FileNotFoundError:
            print("File 'keyboard_log.txt' not found.")

        time.sleep(3)

running = True

typing_enabled = False

def on_press(key):
    global running
    global typing_enabled

    if key == Key.esc:
        running = False

    try:
        if key.char == 'q':
            typing_enabled = not typing_enabled
    except AttributeError:
        pass

listener_thread = threading.Thread(target=lambda: Listener(on_press=on_press).start())

listener_thread.start()

main_loop()

typing_enabled = False

listener_thread.join()
