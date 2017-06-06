import subprocess, pyautogui, os, sys, json, msvcrt
import win32con, ctypes, ctypes.wintypes
from tkinter.filedialog import askopenfilename

config_file = "CONFIG"

def start_paladins(steam_path):
    subprocess.call([steam_path, "-applaunch", "444090"])
    return

def close_paladins():
    return

# vkcodes
# https://gist.github.com/chriskiehl/2906125

def record_mouse_positions():
    # https://stackoverflow.com/questions/15777719/how-to-detect-key-press-when-the-console-window-has-lost-focus
    # Author: Jammerx2

    count = 0
    coordinates = []
    ctypes.windll.user32.RegisterHotKey(None, 1, 0, 0x41) # register A (0x41) as key we're listening for

    try:
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

            if msg.message == win32con.WM_HOTKEY:
                coordinate = pyautogui.position()
                print("Recorded mouse coordinated: ", coordinate)
                coordinates.append(coordinate)
                count += 1

                if (count == 2):
                    break

            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))

    finally:
        ctypes.windll.user32.UnregisterHotKey(None, 1)

    return coordinates


def execute_click_series(coordinates):
    return

if __name__ == "__main__":

    if not os.path.isfile(config_file):
        with open(config_file, "w+") as json_config:
            steam_path = askopenfilename(title="Navigate to your steam folder and select the 'Steam.exe' file.")
            if (len(steam_path) == 0):
                print("No file selected, exitting.")
                json_config.close()
                os.remove(config_file)
                sys.exit(0)

            start_paladins(steam_path)

            coordinates = record_mouse_positions()

            data = {
                "path": steam_path,
                "coordinates": coordinates
            }

            json.dump(data, json_config)
            json_config.close()

    with open(config_file) as json_config:
        py_dict = json.load(json_config)
        path = py_dict['path']
        coordinates = py_dict['coordinates']

        start_paladins(steam_path)
        execute_click_series(coordinates)
