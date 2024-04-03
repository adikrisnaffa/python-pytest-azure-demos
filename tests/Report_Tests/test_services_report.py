import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture()
def setup():
    driver = None
    try:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get("https://apps.pertamina.com/ivendordev/")
        driver.implicitly_wait(3)

        # Login
        username = driver.find_element(By.ID, "Loginid")
        username.send_keys("admin")
        password = driver.find_element(By.ID, "Password")
        password.send_keys("admin")
        button_login = driver.find_element(By.ID, "btnlogin")
        button_login.click()
        time.sleep(3)

        # close modal pop up
        button_modal = driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
        button_modal.click()
        time.sleep(5)

        yield driver 
    finally:
        if driver:
            driver.quit()

#==================================================================================================================================================================
# ASSERTION
#==================================================================================================================================================================
def test_title_assertion(setup):
    Title = setup.title
    assert Title == "iVendor - Home"

#==================================================================================================================================================================
# SCENARIO / TESTCASE 2 : MEMBUKA DROPDOWN MASTER DATA
#==================================================================================================================================================================


#==================================================================================================================================================================
# SCENARIO / TESTCASE 3 : MEMBUKA SEMUA LIST DROPDOWN DARI MASTER MENU
#==================================================================================================================================================================

@pytest.mark.reportmenu
def test_open_and_verify_report_pages(setup):
    # Daftar nama menu dalam dropdown Report
    report_menu_items = [
        "SLA Details",
        "SLA Summary",
        "SLA ICT Details",
        "SLA ICT Summary",
        "PPh 15",
        "PPh 22",
        "PPh 4(2)",
        "PPh 21 NE",
        "PPh 23 & 26",
        "Report SKK",
        "Report VIM",
        "Bukti Potong PPh"
    ]

    # Daftar nama menu dalam dropdown Report
    title_names = [
        "iVendor - Report SLA Details",
        "iVendor - Report SLA Summary",
        "iVendor - Report SLA ICT Details",
        "iVendor - Report SLA ICT Summary",
        "iVendor - Report PPh 15",
        "iVendor - Report PPh 22 Produk",
        "iVendor - Report PPh 4 Ayat 2",
        "iVendor - Report PPh 21 NE",
        "iVendor - Report PPh 23 & 26",
        "iVendor - Report SKK",
        "iVendor - Report VIM",
        "iVendor - Bukti Potong PPh"
    ]

    # Membuka dropdown Report
    report_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-report']")
    report_dropdown.click()
    time.sleep(1)  # Tunggu sebentar untuk dropdown muncul

    # Melakukan iterasi pada setiap menu dalam dropdown Report
    for menu_item in report_menu_items:
        # Mendapatkan elemen menu berdasarkan teksnya
        menu_element = setup.find_element(By.XPATH, f"//a/span[contains(text(), '{menu_item}')]")
        
        # Mengklik menu
        menu_element.click()
        time.sleep(1) 

        current_title = setup.title
        print(f"Judul halaman saat ini: {current_title}")
        assert any(title in current_title for title in title_names), f"Salah satu halaman dari {title_names} tidak dimuat dengan benar"

        # Verifikasi bahwa halaman yang dimuat sesuai dengan menu yang diklik
        assert any(title in setup.title for title in title_names), f"Salah satu halaman dari {title_names} tidak dimuat dengan benar"

