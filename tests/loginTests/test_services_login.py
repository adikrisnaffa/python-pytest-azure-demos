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

    #==================================================================================================================================================================
    # ASSERTION
    #==================================================================================================================================================================
    def test_title_assertion(self, setup):
        Title = setup.title
        assert Title in "iVendor - Login"

    #==================================================================================================================================================================
    # SCENARIO / TESTCASE 1 : LOGIN DENGAN USERNAME YANG BENAR DAN PASSWORD YANG BENAR
    #==================================================================================================================================================================
    def test_login_success(self, setup):
        username = setup.find_element(By.ID, "Loginid")
        username.send_keys("admin")
        password = setup.find_element(By.ID, "Password")
        password.send_keys("admin")
        button_login = setup.find_element(By.ID, "btnlogin")
        button_login.click()
        time.sleep(3)

        Title = setup.title
        assert Title in "iVendor - Home"

    #==================================================================================================================================================================
    # SCENARIO / TESTCASE 2-3-4 : LOGIN DENGAN KOMBINASI INPUT VALUE YANG SALAH
    #==================================================================================================================================================================
    Kunci = [
        ("admin","asdfghj"),        #username benar password salah
        ("asdfghj","admin"),        #username salah password benar
        ("asdfghj","asdfghj")       #username salah password salah
    ]

    @pytest.mark.negativetest
    @pytest.mark.parametrize('a,b' , Kunci)
    def test_loginfailed(self, setup, a, b):
        username = setup.find_element(By.ID, "Loginid")
        username.send_keys(a)
        password = setup.find_element(By.ID, "Password")
        password.send_keys(b)
        button_login = setup.find_element(By.ID, "btnlogin")
        button_login.click()
        time.sleep(5)

        InvalidTextXPaths  = [
            "//div[contains(text(),'Password tidak tepat!')]",
            "//div[contains(text(),'User Tidak Ditemukan!')]",
            "//div[contains(text(),'User Tidak Ditemukan!')]"
        ]

        invalid_messages = []

        for xpath in InvalidTextXPaths:
            elements = setup.find_elements(By.XPATH, xpath)
            
            if elements:
                invalid_messages.append(elements[0].text)   

        assert "Password tidak tepat!" in invalid_messages
        assert "User Tidak Ditemukan!" in invalid_messages

        assert len(invalid_messages) == 2
