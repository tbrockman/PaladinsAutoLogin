import subprocess, pyautogui, os, sys, json, msvcrt, time
import win32con, ctypes, ctypes.wintypes
import tkinter, win32api, pywintypes
from tkinter.filedialog import askopenfilename

config_file = "CONFIG"

def load_config_file():
    with open(config_file) as json_config:
        try:
            py_dict = json.load(json_config)
            json_config.close()
            return py_dict

        except:
            print("Error loading config file, verify CONFIG is properly formatted JSON.")
            json_config.close()
            sys.exit(1)


def start_paladins(steam_path):
    return subprocess.call([steam_path, "-applaunch", "444090"])

def close_paladins():
    return os.system('taskkill /f /im Paladins.exe')

# vkcodes
# https://gist.github.com/chriskiehl/2906125

def click_coordinates(coordinates):
    for i in range(len(coordinates)):
        time.sleep(60)
        pyautogui.click(coordinates[i])

    return

def create_label(text):
    label = tkinter.Label(text=text, font=('Arial','80'), fg='white', bg='black', justify="center", wraplength=1500)
    label.master.overrideredirect(True)
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()
    label.update_idletasks()
    label.update()

def record_mouse_positions():
    # https://stackoverflow.com/questions/15777719/how-to-detect-key-press-when-the-console-window-has-lost-focus
    # Author: Jammerx2

    count = 0
    coordinates = []
    ctypes.windll.user32.RegisterHotKey(None, 1, 0, 0x41) # register A (0x41) as key we're listening for

    try:
        msg = ctypes.wintypes.MSG()
        create_label('Move your mouse over the play button and then press "a" on your keyboard.')

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

if __name__ == "__main__":

    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file)

    if not os.path.isfile(config_file):
        with open(config_file, "w+") as json_config:
            steam_path = askopenfilename(title="Navigate to your Steam folder and select 'Steam.exe'")
            if (len(steam_path) == 0):
                print("No file selected, exitting.")
                json_config.close()
                os.remove(config_file)
                sys.exit(1)

            start_paladins(steam_path)

            coordinates = record_mouse_positions()

            data = {
                "path": steam_path,
                "coordinates": coordinates
            }

            json.dump(data, json_config)
            json_config.close()

    else:
        py_dict = load_config_file()
        steam_path = py_dict['path']

        if not steam_path:
            print("No path to Steam.exe, verify CONFIG file.")
            sys.exit(1)

        coordinates = py_dict['coordinates']

        if len(coordinates) == 0:
            print("No click coordinates, delete CONFIG and recalibrate.")
            sys.exit(1)

        start_paladins(steam_path)
        click_coordinates(coordinates)
        time.sleep(10)
        close_paladins()
