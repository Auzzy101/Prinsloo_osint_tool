import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def take_screenshot(url, filename):
    try:
        options = Options()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.set_window_size(1920, 1080)
        driver.get(url)

        os.makedirs("screenshots", exist_ok=True)
        filepath = os.path.join("screenshots", filename)
        driver.save_screenshot(filepath)
        print(f"[📸] Screenshot saved: {filepath}")

        driver.quit()
    except WebDriverException as e:
        print(f"[!] Screenshot error: {e}")
