# keylogger

This is my python keylogger!

## Usage

Open 2 tabs if in a terminal

In the first window: `python keylogger.py`

In the second window: `python server.py`

This will now start recording what you are typing and send it to your "server"

## General Notes

Currently, it is setup so the keylogger script looks at 127.0.0.1
This means that the script is not actually trying to send the information over the network, it is doing it all internally.

The keylogger script runs until disabled.

The server script runs until it is sent information and then the server ends.

Your tracked keystrokes are saved under remote.txt in the path that your server script is running at.

The code to automatically replicate the keylogger script in your startup folder is commented out.

This is only currently made for windows.
