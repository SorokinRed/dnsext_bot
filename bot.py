from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import cv2

class DNSExitBot():
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path='chromedriver2.43'
        )
        self.driver.set_window_size(1024, 1200)
        self.wait = WebDriverWait(self.driver, 5)
        
    def click(self, xpath):
        elem = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )
        elem.click()

    def click_by_text(self, value):
        xpath = '//*[contains(text(), "{}")]'.format(value)
        elem = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )
        elem.click()

    def select(self, xpath, value):
        self.click(xpath)
        self.click_by_text(value)

    def open_page(self, url):
        self.driver.get(url)

    def type_text(self, xpath, text):
        elem = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )
        elem.send_keys(text)

    def scroll_to(self, xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", elem)

    def elem_screenshot(self, xpath, filename):
        self.driver.save_screenshot('screen.png')
        elem_img = self.driver.find_element_by_xpath("//img[@name='authidimg']")
        size = elem_img.size
        location = elem_img.location
        img = cv2.imread('screen.png')
        img_crop = img[
            location['y']:location['y']+size['height'],
            location['x']:location['x']+size['width']
        ]
        cv2.imwrite(filename, img_crop)    
