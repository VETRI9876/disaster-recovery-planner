from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get('http://localhost:8085')
        wait = WebDriverWait(driver, 10)

        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        print("✅ H1 tag found:", heading.text)

        driver.find_element(By.ID, "system-name").send_keys("Test System")
        driver.find_element(By.ID, "rto").send_keys("5")
        driver.find_element(By.ID, "rpo").send_keys("2")

        status_dropdown = driver.find_element(By.ID, "status")
        status_dropdown.click()
        time.sleep(1)
        status_option = driver.find_element(By.XPATH, "//div[text()='Ready']")
        status_option.click()

        driver.find_element(By.ID, "add-button").click()
        time.sleep(2)

        table = driver.find_element(By.ID, "table-container")
        assert "Test System" in table.text
        print("✅ Table updated with new system.")

        chart = driver.find_element(By.ID, "status-chart")
        assert chart is not None
        print("✅ Chart is present.")

        driver.quit()

        print("✅ Whole application successfully tested!")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_application()
