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
@pytest.mark.mastermenu
def test_open_master_dropdown(setup):
    # Membuka dropdown master
    master_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-master']")
    master_dropdown.click()
    time.sleep(1) 

    # Verifikasi bahwa dropdown telah terbuka
    master_menu = setup.find_element(By.ID, "nav-menu-master")
    assert master_menu.is_displayed(), "Dropdown master tidak terbuka"

@pytest.mark.mastermenu
def test_master_menu_items(setup):
    # Membuka dropdown master
    master_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-master']")
    master_dropdown.click()
    time.sleep(1)  

    # Mengumpulkan daftar item menu master yang diharapkan
    expected_menu_items = [
        "Data Registrasi",
        "Data SAP Vendor",
        "Data SAP PO",
        "Data SAP SAGR",
        "Dok Mandatory Bast",
        "Dok Mandatory Bast ICT",
        "Logo Perusahaan",
        "Notifikasi Web",
        "Template Email",
        "User Admin",
        "User Mapping",
        "Vendor ICT",
        "Vendor SKK",
        "FAQ",
        "Flag Validasi",
        "Konten Image",
        "Konten Kebijakan",
        "Mapping Approval BAST",
        "Mapping Approval PA",
        "Mapping Menu",
        "User Manual"
    ]

    # Mendapatkan daftar item menu yang sebenarnya dari halaman
    actual_menu_items = setup.find_elements(By.XPATH, "//ul[@id='nav-menu-master']//span")

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
# SCENARIO / TESTCASE 3 : MEMBUKA SEMUA LIST DROPDOWN DARI MASTER MENU
#==================================================================================================================================================================
@pytest.mark.mastermenu
def test_open_and_verify_master_data_pages(setup):
    master_dropdown = setup.find_element(By.CSS_SELECTOR, "a[data-bs-target='#nav-menu-master']")
    master_dropdown.click()
    time.sleep(1)  

    # Daftar nama menu Master Data
    menu_names = [
        "Data Registrasi",
        "Data SAP Vendor",
        "Data SAP PO",
        "Data SAP SAGR",
        "Dok Mandatory Bast",
        "Dok Mandatory Bast ICT",
        "Logo Perusahaan",
        "Notifikasi Web",
        "Template Email",
        "User Admin",
        "User Mapping",
        "Vendor ICT",
        "Vendor SKK",
        "FAQ",
        "Flag Validasi",
        "Konten Image",
        "Konten Kebijakan",
        "Mapping Approval BAST",
        "Mapping Approval PA",
        "Mapping Menu",
        "User Manual"
    ]

    # Daftar nama Title Master Data
    title_names = [
        "iVendor - Data Registrasi",
        "iVendor - Data SAP Vendor",
        "iVendor - Data SAP PO",
        "iVendor - Data SAP SAGR",
        "iVendor - Dokumen Mandatory BAST",
        "iVendor - Dokumen Mandatory BAST ICT",
        "Logo Perusahaan",
        "Notifikasi Web",
        "Template Email",
        "User Admin",
        "User Mapping",
        "Vendor ICT",
        "Vendor SKK",
        "FAQ",
        "Flag Validasi",
        "Konten Image",
        "Konten Kebijakan",
        "Mapping Approval BAST",
        "Mapping Approval PA",
        "iVendor - Menu Mapping",
        "iVendor - User Manual Master"
    ]

    # Melakukan iterasi pada setiap menu
    for menu_name in menu_names:
        time.sleep(1)
        # Mendapatkan elemen menu berdasarkan teksnya
        menu_element = setup.find_element(By.XPATH, f"//a/span[contains(text(), '{menu_name}')]")
        
        # Mengklik menu
        menu_element.click()
        time.sleep(1) 

        current_title = setup.title
        print(f"Judul halaman saat ini: {current_title}")
        assert any(title in current_title for title in title_names), f"Salah satu halaman dari {title_names} tidak dimuat dengan benar"

        # Verifikasi bahwa halaman yang dimuat sesuai dengan menu yang diklik
        assert any(title in setup.title for title in title_names), f"Salah satu halaman dari {title_names} tidak dimuat dengan benar"

