import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestLogin:
    @pytest.fixture()
    def setup(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(10)
            driver.maximize_window()
            driver.get("https://apps.pertamina.com/ivendordev/")
            driver.implicitly_wait(3)
            yield driver 
        finally:
            driver.quit()

    def login(driver):
        username = driver.find_element(By.ID, "Loginid")
        username.send_keys("admin")
        password = driver.find_element(By.ID, "Password")
        password.send_keys("admin")
        button_login = driver.find_element(By.ID, "btnlogin")
        button_login.click()
        time.sleep(3)


