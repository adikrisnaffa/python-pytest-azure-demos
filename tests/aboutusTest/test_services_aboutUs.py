import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestAboutUs:
    @pytest.fixture()
    def test_setup(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')

            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(10)
            driver.maximize_window()
            yield driver 
        finally:
            driver.quit()

    def test_AboutUs(self, test_setup):
        driver = test_setup
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys("adminadminadmin")
        driver.find_element(By.NAME, "password").send_keys("adminadminadmin")
        driver.find_element(By.NAME, "username").submit()
        assert "ParaBank | Error" in driver.title

        driver.find_element(By.XPATH, "//a[text()='About Us']").click()
        assert "ParaBank | About Us" in driver.title

        driver.find_element(By.LINK_TEXT, "Log Out").click()
