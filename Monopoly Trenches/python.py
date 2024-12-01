import cv2
import numpy as np
import pyautogui
import time
import os

ImageFolderPath = r"---------------------------enter your image folder path----------------------"

def find_and_click_images(image_folder, threshold=0.8, click_positions_mapping=None, counters=None):
    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)

        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            continue

        w, h = template.shape[::-1]
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            pt = max_loc

            if image_name == "TableSelection.png":
                fixed_x, fixed_y = 957, 891
                pyautogui.click(fixed_x, fixed_y)
                time.sleep(1)
                pyautogui.click(fixed_x, fixed_y)
            elif image_name == "MonopolyGoatScammer.png":
                pyautogui.click(pt[0] + w // 2, pt[1] + h // 2)
                time.sleep(0.5)  # Wait for half a second
                pyautogui.click(1714, 981)  # Click the second location after waiting
                counters["Check/All In"] += 1  # Increment counter for Check/All In
            elif image_name == "LowOnChips.png":
                counters["Low on chips"] += 1  # Increment counter for Low on chips
                if image_name in click_positions_mapping:
                    click_x, click_y = click_positions_mapping[image_name]
                    pyautogui.click(click_x, click_y)
                else:
                    center_x, center_y = pt[0] + w // 2, pt[1] + h // 2
                    pyautogui.click(center_x, center_y)
            else:
                if image_name in click_positions_mapping:
                    click_x, click_y = click_positions_mapping[image_name]
                    pyautogui.click(click_x, click_y)
                else:
                    center_x, center_y = pt[0] + w // 2, pt[1] + h // 2
                    pyautogui.click(center_x, center_y)
            break

def print_counters(counters):
    print("------------")
    print(f"Low on chips: {counters['Low on chips']}")
    print(f"Check/All in: {counters['Check/All In']}")
    print("------------")

if __name__ == "__main__":
    image_folder = ImageFolderPath
    if not os.path.exists(image_folder):
        exit(1)

    click_positions_mapping = {
        "LowOnChips.png": (709, 726),
        "BrokeBoyAlert.png": (1439, 202),
        "MainMenuAlert.png": (176, 516),
        "MonopolyGoatScammer.png": (1437, 980),
    }

    counters = {
        "Low on chips": 0,
        "Check/All In": 0
    }

    while True:
        try:
            find_and_click_images(image_folder, threshold=0.8, click_positions_mapping=click_positions_mapping, counters=counters)
        except Exception as e:
            pass
        print_counters(counters)  # Print the counts
        time.sleep(1)
