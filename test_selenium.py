from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_application():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        # Create a unique user data dir for each run to avoid lock issues
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")

        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get('http://localhost:8085')

        time.sleep(2)

        element = driver.find_element(By.TAG_NAME, 'h1')  # Update tag as per your page
        if element:
            print("✅ Success: Element found:", element.text)
        else:
            print("❌ Error: Element not found.")

        driver.quit()

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_application()
