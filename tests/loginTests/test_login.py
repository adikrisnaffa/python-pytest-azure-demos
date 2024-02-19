import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestLogin:
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

    def test_01_login(self, test_setup):
        driver = test_setup
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys("adminadmin")
        driver.find_element(By.NAME, "password").send_keys("demodemo")
        driver.find_element(By.NAME, "username").submit()
        assert "ParaBank | Accounts Overview" in driver.title

    def test_02_login_fail_test(self, test_setup):
        driver = test_setup
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        driver.find_element(By.NAME, "username").submit()
        assert "ParaBank | Error" in driver.title

    def test_03_login_fail_test(self, test_setup):
        driver = test_setup
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin")
        driver.find_element(By.NAME, "username").submit()
        assert "ParaBank | Error" in driver.title

    def test_04_login_fail_test(self, test_setup):
        driver = test_setup
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        driver.find_element(By.NAME, "username").submit()
        assert "ParaBank | Error" in driver.title
