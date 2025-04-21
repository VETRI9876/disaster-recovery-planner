from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_application():
    try:
        # Set up Chrome WebDriver (with Selenium and ChromeDriver)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Navigate to the URL of your application
        driver.get('http://localhost:8085')  # Adjust this URL if needed for your app

        # Wait for the page to load
        time.sleep(2)

        # Check if a specific element exists (you can change the selector)
        element = driver.find_element(By.TAG_NAME, 'h1')  # Replace with your actual element
        if element:
            print("Success: The page loaded and the element was found!")
        else:
            print("Error: The element was not found.")
        
        # Close the browser
        driver.quit()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_application()
