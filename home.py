import sys
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal

from main import swipe_read_until_100, run
# from classKteam import *
import subprocess
import asyncio


def get_connected_devices():
    try:
        result = subprocess.run(['adb', 'devices', '-l'], capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()

        # Extract serial numbers
        serial_numbers = [line.split()[0] for line in output_lines[1:] if 'device' in line]

        return serial_numbers
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []


# Get the list of connected devices
connected_devices = get_connected_devices()


# Print the list of serial numbers
# print("Connected Devices:")
# for device in connected_devices:
#     print(device)

# async def my_async_function(device):
#     print(f"Start processing: {device}")
#     # await asyncio.sleep(2)  # Simulate some asynchronous operation
#     # print(f"Finish processing: {arg}")
#
# async def main():
#     tasks = [my_async_function(device) for device in connected_devices]
#     await asyncio.gather(*tasks)

class MyApplication(QWidget):
    def __init__(self):
        super().__init__()

        # Create widget and layout
        self.init_ui()

    def init_ui(self):
        # Create UI components
        self.edit_text1 = QLineEdit(self)
        self.edit_text2 = QLineEdit(self)
        self.button = QPushButton('Click me', self)

        # Create layout and add components to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit_text1)
        layout.addWidget(self.edit_text2)
        layout.addWidget(self.button)

        # Set layout for the main widget
        self.setLayout(layout)

        # Connect button click event to the handler function
        self.button.clicked.connect(self.on_button_click)

        # Set window size and display
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('auto read book')
        self.show()

    def on_button_click(self):
        # Handle the button click event
        user_input1 = self.edit_text1.text()
        user_input2 = self.edit_text2.text()
        print(f'User input 1: {user_input1}')
        print(f'User input 2: {user_input2}')

        # Add your logic here using user_input1 and user_input2
        # ...

        for device in connected_devices:
            print(device)
            p1 = threading.Thread(target=run, args=(int(user_input1), int(user_input2), device))
            p1.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApplication()
    sys.exit(app.exec_())
