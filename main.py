import subprocess
import time
import re
import cv2
import pytesseract
import subprocess
from PIL import Image
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




def capture_screenshot():
    # Run adb command to capture a screenshot
    adb_command = 'adb exec-out screencap -p > screenshot.png'
    subprocess.run(adb_command, shell=True)
    print('screenshot saved successfully.')

def check_end_of_book(text):
    # Kiểm tra xem văn bản có phải là "Page X of Y" hay không
    try:
        # Kiểm tra xem văn bản có phải là "Page X of Y" hay không
        if "Page" in text and "of" in text:
            page_info = text.split(" ")
            current_page = int(page_info[1])
            total_pages = int(page_info[3])

            if current_page == total_pages:
                return True
        return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra cuối sách: {e}")
        return False
def find_text_in_screenshot():
    capture_screenshot()
    # Read the screenshot using OpenCV
    screenshot = cv2.imread('screenshot.png')

    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("gray_image.png", gray)
    # show_gray_image(gray)
    # cv2.waitKey(0)

    # Use pytesseract to extract text from the image
    bottom_cropped = gray[-100:, :]

    text = pytesseract.image_to_string(bottom_cropped, lang='eng')

    result = check_end_of_book(text.strip())

    print("text fonund:"+text+" "+str(result))
    # Check if "100%" is present in the extracted text
    return result
def is_screen_off_text_100():
    # Implement the logic to check if the screen off text is 100%
    # You may need to run another adb command to get the current state
    return find_text_in_screenshot()


def press_back_key():
    # Run the ADB command to simulate a "back" key press
    subprocess.run("adb shell input keyevent KEYCODE_BACK", shell=True, check=True)
def swipe_read_until_100(timeout_seconds=3):
    start_time = time.time()

    read=is_screen_off_text_100()
    while not read:
        if read:
            print("read done")

            return

        else:
            time.sleep(3)  # Adjust the sleep time as needed
            # Run the swipe_read function with your desired coordinates
            swipe_read(500, heightScree / 2, 100, heightScree / 2)
            time.sleep(1)

        read = is_screen_off_text_100()

       # Adjust the sleep time as needed

    print("read done")



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def readBook():
    swipe_read_until_100()
    time.sleep(3)
    press_back_key()


readBook()
