import pytesseract
from PIL import ImageGrab
import re
import pyautogui
import time
import pyscreeze
import json
import pyperclip
from pod_checker import is_bar_almost_full

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
green_bar_region = (832, 1026, 1304, 1035)  
search_region = (432, 64, 1025, 672)

def load_script(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_zaaps(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

zaaps = load_zaaps('zaap.json')['zaaps']

def find_nearest_zaap(target_coord, zaaps):
    closest_zaap = None
    min_distance = float('inf')
    for zaap in zaaps:
        zaap_coord = (zaap['location']['x'], zaap['location']['y'])
        distance = calculate_distance(target_coord, zaap_coord)
        print(f"Checking zaap: {zaap['name']} at {zaap_coord}, distance: {distance}")  
        if distance < min_distance:
            min_distance = distance
            closest_zaap = zaap
    print(f"Nearest zaap: {closest_zaap['name']} at distance: {min_distance}")  
    return closest_zaap

def calculate_distance(coord1, coord2):
    return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

def is_too_far(current_coord, target_coord):
    distance = calculate_distance(current_coord, target_coord)
    return distance > DISTANCE_THRESHOLD    

def move_to_target(current_coord, target_coord, nearest_zaap):
    global current_coordinates  

    if nearest_zaap:
        print(f"Teleporting using zaap: {nearest_zaap['name']}")

        pyperclip.copy(nearest_zaap['name'])

        pyautogui.press('h')
        time.sleep(2)
        click_on_png_and_wait_for_change("bank/zaap.png", 2, search_region)
        pyautogui.click(x=1135, y=237)  
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'v')  
        time.sleep(2)

        tp_location = pyautogui.locateCenterOnScreen("bank/tp.png", confidence=0.8)
        if tp_location:
            pyautogui.click(tp_location)
            print(f"Teleported to: {nearest_zaap['name']}")
            time.sleep(2)

            current_coordinates = [nearest_zaap['location']['x'], nearest_zaap['location']['y']]
            print(f"Updated current coordinates after teleportation: {current_coordinates}")
        else:
            print("Teleport image 'tp.png' not found.")
    else:
        print("No nearest zaap found.")

def extract_coordinates(text):
    match = re.search(r"(-?\d+),(-?\d+)", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

def calculate_movements(current, target):
    x_movement = target[0] - current[0]
    y_movement = target[1] - current[1]
    return x_movement, y_movement

def get_current_coordinates():
    region = (13, 40, 308, 154)
    screenshot = ImageGrab.grab(bbox=region)
    extracted_text = pytesseract.image_to_string(screenshot)
    return extract_coordinates(extracted_text)

def wait_for_map_change(expected_coordinates):
    while True:
        current_coordinates = get_current_coordinates()
        if current_coordinates == expected_coordinates:
            break
        time.sleep(1)

def click_on_png_and_wait_for_change(png_path, sleep_time, search_region):
    try:
        location = pyautogui.locateCenterOnScreen(png_path, region=search_region, confidence=0.6)
        if location is not None:
            pyautogui.click(location)
            time.sleep(sleep_time)
    except pyautogui.ImageNotFoundException:
        print("Image not found.")

def specific_actions():

    pyautogui.press('h')

    time.sleep(2)

    try:
        zaap_location = pyautogui.locateCenterOnScreen("bank/zaap.png", confidence=0.8)
        if zaap_location is not None:
            pyautogui.click(zaap_location)
            print("Clicked on the Zaap")
            time.sleep(2)

            pyautogui.click(x=1135, y=237)
            time.sleep(2)

            pyperclip.copy("Cité d'Astrub")
            pyautogui.hotkey('ctrl', 'v')  
            time.sleep(2)

            pyautogui.click(x=833, y=326)
            time.sleep(2)

            tp_location = pyautogui.locateCenterOnScreen("bank/tp.png", confidence=0.8)
            if tp_location is not None:
                pyautogui.click(tp_location)
                print("Clicked on the teleport")
                time.sleep(2)

                current_coordinates = get_current_coordinates()
                if current_coordinates:

                    x_move, y_move = calculate_movements(current_coordinates, (4, -18))

                    execute_movements_with_pause(x_move, y_move, current_coordinates, jobs, search_region)

                    door_location = pyautogui.locateCenterOnScreen("bank/porte.png", confidence=0.8)
                    if door_location is not None:
                        pyautogui.click(door_location)
                        print("Clicked on the Door")
                        time.sleep(5)

                        bank_pnj_location = pyautogui.locateCenterOnScreen("bank/pnj_bank.png", confidence=0.8)
                        if bank_pnj_location is not None:
                            pyautogui.click(bank_pnj_location)
                            print("Clicked on the bank NPC")
                            time.sleep(2)

                            top_left_x, top_left_y = 786, 748
                            bottom_right_x, bottom_right_y = 1021, 768
                            click_x = (top_left_x + bottom_right_x) // 2
                            click_y = (top_left_y + bottom_right_y) // 2
                            pyautogui.click(click_x, click_y)
                            print(f"Clicked inside the region at ({click_x}, {click_y})")
                            time.sleep(4)

                            new_top_left_x, new_top_left_y = 1257, 140
                            new_bottom_right_x, new_bottom_right_y = 1274, 156
                            new_click_x = (new_top_left_x + new_bottom_right_x) // 2
                            new_click_y = (new_top_left_y + new_bottom_right_y) // 2
                            pyautogui.click(new_click_x, new_click_y)
                            print(f"Clicked inside the new region at ({new_click_x}, {new_click_y})")
                            time.sleep(4)

                            region_to_capture = (1247, 133, 1575, 234)  
                            screenshot = ImageGrab.grab(bbox=region_to_capture)

                            extracted_text = pytesseract.image_to_string(screenshot)
                            print("Extracted text:", extracted_text)  

                            if "Transférer tous les objets" in extracted_text:

                                click_x = (region_to_capture[0] + region_to_capture[2]) // 2
                                click_y = (region_to_capture[1] + region_to_capture[3]) // 2
                                pyautogui.click(click_x, click_y)
                                print(f"Clicked at ({click_x}, {click_y}) in the region")
                                time.sleep(2)

                                new_top_left_x, new_top_left_y = 1554, 108
                                new_bottom_right_x, new_bottom_right_y = 1566, 119
                                new_click_x = (new_top_left_x + new_bottom_right_x) // 2
                                new_click_y = (new_top_left_y + new_bottom_right_y) // 2
                                pyautogui.click(new_click_x, new_click_y)
                                print(f"Clicked inside the new region at ({new_click_x}, {new_click_y})")
                                time.sleep(2)
                        else:
                            print("The bank NPC cannot be found")
                    else:
                        print("The Door cannot be found")

                else:
                    print("Current coordinates not found.")
            else:
                print("The teleport cannot be found")

        else:
            print("The Zaap cannot be found")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_and_act_on_green_bar():

    if is_bar_almost_full(green_bar_region, threshold=80):
        print("Green bar is at least 80% full. Performing specific actions.")
        specific_actions()
    else:
        print("Green bar is not yet 80% full.")

def execute_movements_with_pause(x_movement, y_movement, current_coordinates, jobs, search_region):

    up_region = (386, 23, 1170, 15)
    down_region = (407, 906, 1067, 16)
    left_region = (325, 42, 26, 858)
    right_region = (1570, 45, 17, 847)
    action_delay = 0.5

    def interact_with_resource(location):
        pyautogui.click(location)
        time.sleep(8)

    job_images = {
        'orthie': {'images': ['ortie/orthie.png'], 'confidence': 0.8},
        'frene': {'images': ['bois/frene.png', 'bois/frene2.png', 'bois/frene3.png', 'bois/frene4.png'], 'confidence': 0.8},
        'ble': {'images': ['paysan/ble.png','paysan/ble2.png','paysan/ble3.png'], 'confidence': 0.8}
    }

    def check_for_and_interact_with_images():
        for job in jobs:
            job_info = job_images.get(job, {})
            for image_name in job_info.get('images', []):
                interact_with_images(image_name, interact_with_resource, search_region, job_info.get('confidence', 0.8))

    def interact_with_images(image_name, interaction_function, search_region, confidence):
        while True:
            found = False
            try:
                for location in pyautogui.locateAllOnScreen(image_name, region=search_region, confidence=confidence):
                    print("Resource Found!")
                    interaction_function(pyautogui.center(location))
                    found = True
                    break
            except pyscreeze.ImageNotFoundException:
                pass

            if not found:
                break

    for _ in range(abs(y_movement)):
        expected_coordinates = (current_coordinates[0], current_coordinates[1] + (-1 if y_movement < 0 else 1))
        if y_movement < 0:
            pyautogui.click(x=up_region[0] + up_region[2] // 2, y=up_region[1] + up_region[3] // 2)
        else:
            pyautogui.click(x=down_region[0] + down_region[2] // 2, y=down_region[1] + down_region[3] // 2)
        time.sleep(action_delay)
        wait_for_map_change(expected_coordinates)
        check_for_and_interact_with_images()
        current_coordinates = expected_coordinates

    for _ in range(abs(x_movement)):
        expected_coordinates = (current_coordinates[0] + (-1 if x_movement < 0 else 1), current_coordinates[1])
        if x_movement < 0:
            pyautogui.click(x=left_region[0] + left_region[2] // 2, y=left_region[1] + left_region[3] // 2)
        else:
            pyautogui.click(x=right_region[0] + right_region[2] // 2, y=right_region[1] + right_region[3] // 2)
        time.sleep(action_delay)
        wait_for_map_change(expected_coordinates)
        check_for_and_interact_with_images()
        current_coordinates = expected_coordinates

script = load_script('script.json')
jobs = script['jobs']
map_coordinates = script['maps']
DISTANCE_THRESHOLD = 20  
current_coordinates = get_current_coordinates()
print(f"Starting at: {current_coordinates}")  

if not current_coordinates:
    print("Current coordinates not found.")
    exit()

while True:
    for target_coordinates in map_coordinates:
        print(f"Moving to map: {target_coordinates}")

        nearest_zaap = find_nearest_zaap(target_coordinates, zaaps)
        distance = calculate_distance(current_coordinates, target_coordinates)
        print(f"Distance to target: {distance}, Threshold: {DISTANCE_THRESHOLD}")  

        if distance > DISTANCE_THRESHOLD:
            print("Using zaap for long distance.")
            move_to_target(current_coordinates, target_coordinates, nearest_zaap)
        else:
            print("Moving directly for short distance.")
            x_move, y_move = calculate_movements(current_coordinates, target_coordinates)
            execute_movements_with_pause(x_move, y_move, current_coordinates, jobs, search_region)
            current_coordinates = target_coordinates

        check_and_act_on_green_bar()