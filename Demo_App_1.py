from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import selenium
from selenium.common.exceptions import NoSuchElementException
import time
from PIL import Image
import io



capabilities = dict(
    platformName = 'Android',
    automationName='uiautomator2',
    udid = "emulator-5554"
)

appium_server_url = "http://localhost:4723"

class TestAppium():
    driver = webdriver.Remote(appium_server_url,capabilities)
    ele_1 = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Life Quotes']")
    print(f"The text on the button is ---> {ele_1.text}")
    ele_1.click()
    time.sleep(8)
    # all category
    def get_text_category(self):
        category_elements = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        print(f"Total categories --> {len(category_elements)}")
        for category_element in category_elements:
            print(category_element.text)
    
    

    # def get_images_category(self):
        # print("I am inside images function")
        img_elements = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")
        
        screenshot = self.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))

        for index,element in enumerate(img_elements):
            cropped_image = image.crop((element.location['x'] , element.location['y'],
                        element.location['x']+element.size['width'],
                        element.location['y']+element.size['height'],
                        ))
            cropped_image.save(f'element_{index}.png')
        

    driver.quit()

obj_1 = TestAppium()
obj_1.get_text_category()
time.sleep(3)
obj_1.get_images_category()






