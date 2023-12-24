import subprocess
import time
import re
import cv2
import pytesseract
import subprocess

from showImage import show_gray_image


def click_point(x, y):
    # Construct the adb command to simulate a tap at the specified coordinates
    adb_command = f'adb shell input tap {x} {y}'

    try:
        # Execute the adb command
        subprocess.run(adb_command, shell=True, check=True)
        print(f"Clicked at ({x}, {y})")
        time.sleep(1)  # Add a delay to ensure the click is registered
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


WidthScree=0
heightScree=0
def get_screen_size():
    # Run the adb command to get display information
    adb_command = 'adb shell wm size'
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

    # Parse the output to extract width and height
    match = re.search(r'(\d+)x(\d+)', result.stdout)
    if match:
        width, height = map(int, match.groups())
        print(f"Screen size: {width}x{height}")
        WidthScree=width
        heightScree=height
        return width, height
    else:
        print("Error: Unable to retrieve screen size.")
        return None

# Example usage: Get and print the screen size

def swipe_read(a_x, a_y, b_x, b_y, duration_ms=500):
    # Construct the adb command to simulate a swipe
    adb_command = f'adb shell input swipe {a_x} {a_y} {b_x} {b_y} {duration_ms}'

    try:
        # Execute the adb command
        subprocess.run(adb_command, shell=True, check=True)
        print(f"Swiped from ({a_x}, {a_y}) to ({b_x}, {b_y})")
        time.sleep(1)  # Add a delay to ensure the swipe is completed
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
# Example usage: Click at coordinates (100, 200)
# click_point(100, 200)

get_screen_size()


import time


def capture_screenshot():
    # Run adb command to capture a screenshot
    adb_command = 'adb exec-out screencap -p > screenshot.png'
    subprocess.run(adb_command, shell=True)


def find_text_in_screenshot():
    capture_screenshot()
    # Read the screenshot using OpenCV
    screenshot = cv2.imread('screenshot.png')

    # Convert the screenshot to grayscale for better text extraction
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("gray_image.png", gray)
    # show_gray_image(gray)
    # cv2.waitKey(0)

    # Use pytesseract to extract text from the image
    # text = pytesseract.image_to_string(gray)

    text = pytesseract.image_to_string(gray, lang='eng')

    print("text fonund "+text)
    # Check if "100%" is present in the extracted text
    return 'review this book on amazon' in text
def is_screen_off_text_100():
    # Implement the logic to check if the screen off text is 100%
    # You may need to run another adb command to get the current state
    find_text_in_screenshot()


def swipe_read_until_100(timeout_seconds=3):
    start_time = time.time()

    # while not is_screen_off_text_100():
    while True:
        time.sleep(3)  # Adjust the sleep time as needed
        # Run the swipe_read function with your desired coordinates
        swipe_read(500, heightScree/2, 100, heightScree/2)
        time.sleep(1)  # Adjust the sleep time as needed


# Example usage: Run the swipe_read_until_100 function
# swipe_read_until_100(timeout_seconds=300)
# find_text_in_screenshot()

# swipe_read_until_100()