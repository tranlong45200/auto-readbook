import re
import subprocess
import time

import cv2

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


WidthScree = 0
heightScree = 0


def get_screen_size(device):
    # Run the adb command to get display information
    adb_command = f'adb -s {device} shell wm size'
    result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

    # Parse the output to extract width and height
    match = re.search(r'(\d+)x(\d+)', result.stdout)
    if match:
        width, height = map(int, match.groups())
        print(f"Screen size: {width}x{height}")
        WidthScree = width
        heightScree = height
        return width, height
    else:
        print("Error: Unable to retrieve screen size.")
        return None


# Example usage: Get and print the screen size

def adb_click(x, y, device):
    adb_command = f"adb -s {device} shell input tap {x} {y}"
    subprocess.run(adb_command, shell=True)


def swipe_read(device, a_x, a_y, b_x, b_y, duration_ms=100):
    # Construct the adb command to simulate a swipe
    adb_command = f'adb -s {device} shell input swipe {a_x} {a_y} {b_x} {b_y} {duration_ms}'

    try:
        # Execute the adb command
        subprocess.run(adb_command, shell=True, check=True)
        print(f"Swiped from ({a_x}, {a_y}) to ({b_x}, {b_y})")
        time.sleep(1)  # Add a delay to ensure the swipe is completed
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def capture_screenshot(device):
    # Run adb command to capture the entire screen
    adb_command = f'adb -s {device} exec-out screencap -p > screenshot_{device}.png'
    subprocess.run(adb_command, shell=True)

    # # Capture successful, now crop the image to include only the relevant area (bottom sheet)
    # crop_command = f'convert screenshot_full_{device}.png -crop WxH+X+Y screenshot_{device}.png'
    # subprocess.run(crop_command, shell=True)

    print('Screenshot saved successfully.')


def check_end_of_book(text):
    # Kiểm tra xem văn bản có phải là "Page X of Y" hay không
    try:
        # Kiểm tra xem văn bản có phải là "Page X of Y" hay không
        if "Page" in text and "of" in text:
            page_info = text.split(" ")
            current_page = int(page_info[1])
            total_pages = int(page_info[3])

            if current_page >= total_pages - 2:
                return True
        return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra cuối sách: {e}")
        return False


indexFail = 0


def find_text_in_screenshot(device):
    global indexFail
    capture_screenshot(device)
    # Read the screenshot using OpenCV
    screenshot = cv2.imread(f'screenshot_{device}.png')

    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(f"gray_image{device}.png", gray)
    # show_gray_image(gray)
    # cv2.waitKey(0)

    # Use pytesseract to extract text from the image
    bottom_cropped = gray[-125:-10, :]

    text = pytesseract.image_to_string(bottom_cropped, lang='eng')

    result = check_end_of_book(text.strip())

    if (result == False and str(text) != "" and not ("Page" in text) and not ("of" in text)):
        result = True

    if ("Learn more" in text) and not ("Share" in text):
        result = False

    print("text fonund:" + text + " " + str(result))

    # Check if "100%" is present in the extracted text
    return result


def is_screen_off_text_100(device):
    # Implement the logic to check if the screen off text is 100%
    # You may need to run another adb command to get the current state
    return find_text_in_screenshot(device)


def press_back_key(device):
    # Run the ADB command to simulate a "back" key press
    adb_command = f"adb -s {device} shell input keyevent KEYCODE_BACK"
    subprocess.run(adb_command, shell=True, check=True)
    # subprocess.run("adb -s{device} shell input keyevent KEYCODE_BACK", shell=True, check=True)


import random


def swipe_read_until_100(device, timeout_seconds=3, timeout_seconds2=3):
    start_time = time.time()

    read = is_screen_off_text_100(device)
    # index0=0
    while not read:
        if read:
            print("read done2")
            return
        else:
            tRandom = random.uniform(timeout_seconds, timeout_seconds2)
            print("wait .... " + str(tRandom))
            time.sleep(tRandom)  # Adjust the sleep time as needed
            # Run the swipe_read function with your desired coordinates
            swipe_read(device, 500, 400, 100, 400)
            time.sleep(1)

        read = is_screen_off_text_100(device)

    # Adjust the sleep time as needed

    print("read done3")


import pytesseract

# executable_path = os.path.dirname(sys.executable)
# tesseract_path = os.path.join(executable_path, 'tesseract.exe')
#
# pytesseract.pytesseract.tesseract_cmd = tesseract_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

# def readBook():
#     swipe_read_until_100()
#     time.sleep(3)
#     press_back_key()


# readBook()

coordinates_list = [
    (140, 311),
    (343, 313),
    (561, 334),
    (138, 640),
    (336, 633),
    (549, 620),
    (135, 953),
    (349, 963),
    (546, 962), ]


# coordinates_list2 = [(135,953),(349,963),(546,962),]

def readBook(coordinates, user_input, user_input2, device):
    # press_back_key(device)
    #
    # return
    # Use coordinates
    x, y = coordinates

    adb_click(x, y, device)
    time.sleep(3)
    # Do something with x and y
    swipe_read_until_100(device, user_input, user_input2)
    time.sleep(2)
    press_back_key(device)
    time.sleep(2)


# Iterate through each set of coordinates and call readBook
def run(user_input, user_input2, device):
    # get_screen_size(device)

    time.sleep(1)

    for coordinates in coordinates_list:
        readBook(coordinates, user_input, user_input2, device)

    time.sleep(2)

    swipe_read(device, 340, 940, 340, 517)

# find_text_in_screenshot("emulator-5554")

# run(1)

# find_text_in_screenshot("127.0.0.1:21503")
