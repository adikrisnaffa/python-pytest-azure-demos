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
# SCENARIO / TESTCASE 2 : MEMBUKA DROPDOWN ICT TRABSACTION DATA
#==================================================================================================================================================================
@pytest.mark.ICTmenu
def test_open_ICT_dropdown(setup):
    # Membuka dropdown ICT
    master_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-transactionict']")
    master_dropdown.click()
    time.sleep(1) 

    # Verifikasi bahwa dropdown telah terbuka
    master_menu = setup.find_element(By.ID, "nav-menu-transactionict")
    assert master_menu.is_displayed(), "Dropdown master tidak terbuka"

    expected_menu_items = [
        "BAST ICT",
        "Invoice ICT",
        "Payment Approval ICT",
        "Tracking ICT"
    ]

    # Mendapatkan daftar item menu yang sebenarnya dari halaman
    actual_menu_items = setup.find_elements(By.XPATH, "//ul[@id='nav-menu-transactionict']//span")

    # Verifikasi bahwa daftar item menu yang diharapkan muncul
    for expected_item_text in expected_menu_items:
        item_found = False
        for actual_item in actual_menu_items:
            if actual_item.text == expected_item_text:
                item_found = True
                break
        assert item_found, f"Item menu '{expected_item_text}' tidak ditemukan"

    # Verifikasi bahwa tidak ada item menu yang tidak diharapkan muncul
    for actual_item in actual_menu_items:
        assert actual_item.text in expected_menu_items, f"Item menu '{actual_item.text}' tidak diharapkan"

    # Cetak semua hasil dari expected_menu_items
    print("Expected Menu Items:")
    for item in expected_menu_items:
        print(item)
        
    # Cetak jumlah item yang diharapkan
    print(f"Total Expected Menu Items: {len(expected_menu_items)}")

    # Cetak jumlah item yang sebenarnya
    print(f"Total Actual Menu Items: {len(actual_menu_items)}")

#==================================================================================================================================================================
# SCENARIO / TESTCASE 3 : MEMBUKA SEMUA LIST DROPDOWN DARI ICT TRABSACTION MENU
#==================================================================================================================================================================
@pytest.mark.ICTmenu
def test_open_and_verify_ict_transaction_pages(setup):
    # Membuka dropdown ICT
    master_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-transactionict']")
    master_dropdown.click()
    time.sleep(1) 

# Daftar nama menu ICT Transaction
    ict_transaction_menu_items = [
        "BAST ICT",
        "Invoice ICT",
        "Payment Approval ICT",
        "Tracking ICT"
    ]

# Daftar nama Title ICT Transaction
    title_names = [
        "iVendor - BAST ICT",
        "iVendor -  Invoice ICT",
        "iVendor - Payment Approval ICT",
        "iVendor - Tracking ICT"
    ]

    # Membuka dropdown ICT Transaction
    ict_transaction_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-transactionict']")
    ict_transaction_dropdown.click()
    time.sleep(1)  

    # Melakukan iterasi pada setiap menu ICT Transaction
    for menu_item in ict_transaction_menu_items:
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
