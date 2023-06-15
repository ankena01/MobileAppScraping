from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import selenium
from selenium.common.exceptions import NoSuchElementException
import time
from PIL import Image
import io

capabilities = dict(
    platformName = 'Android',
    automationName='uiautomator2',
    udid = "emulator-5554",
    # appPackage = 'com.tc.bestquotes',
    # appActivity = 'com.tc.bestquotes.MainActivity'
)

# Starts the Appium Session
driver = webdriver.Remote('http://127.0.0.1:4723', capabilities)

# Method 1 - Using  appPackage and appActivity in desired capabilities
# Method 2 - click the element using locator
ele_1 = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Life Quotes']")
print(f"The text in the icon is {ele_1.text}")
ele_1.click()
time.sleep(5)

elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")

# capture images 

def capture_images(index):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))

    for element in elements:
        cropped_image = image.crop((element.location['x'], element.location['y'],
                    element.location['x'] + element.size['width'],
                    element.location['y'] + element.size['height']))
        cropped_image.save(f'element_{index}.png')
        index = index + 1
    return index

# scrolling functionality

previous_last_element = None
current_index = 0

while True:
    elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")
    time.sleep(3)

    last_element = elements[-1]
    second_element = elements[1]

    if previous_last_element == last_element:
        print("cannot swipe further")
        break
    
    else:
        # logic to get co-ordinates
        last_element_bounds = last_element.get_attribute('bounds')
        # x co-odinate for last element
        last_element_x = last_element_bounds.split("][]")[0:1][0][1:].split(',')[0]
        last_element_x = int(last_element_x)
        # y co-odinate for last element
        # last_element_y = last_element_bounds.split("][]")[0:1][0][1:].split(',')[-1]
        # last_element_y = last_element_bounds.split("][]")[0:1][0][1:].split(',')[-1][:-1]
        # last_element_y = last_element_bounds.split("][]")[0:1][0][1:].split(',')[0:][0]
        last_element_y = last_element_bounds.split("][]")[0:1][0][1:].split(',')[1].split('][')[0]
        last_element_y = int(last_element_y)
        
        second_element_bounds = second_element.get_attribute('bounds')
        
        second_element_x = second_element_bounds.split("][]")[0:1][0][1:].split(',')[0]
        second_element_x = int(second_element_x)
        # y co-odinate for last element
        # second_element_y = second_element_bounds.split("][]")[0:1][0][1:].split(',')[-1]
        second_element_y = second_element_bounds.split("][]")[0:1][0][1:].split(',')[1].split('][')[0]
        second_element_y = int(second_element_y)

        time.sleep(3)

        #  capture images
        current_index = capture_images(index = current_index)
        
        # scroll
        driver.swipe(last_element_x,last_element_y,second_element_x, second_element_y)
        time.sleep(3)
        previous_last_element = last_element

driver.quit()