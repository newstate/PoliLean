from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # If you use WebDriver Manager library
# import time
# import os
# import json

# Use WebDriver Manager to handle ChromeDriver installations/upgrades automatically
# service = Service(ChromeDriverManager().install())

# Initialize the WebDriver
try:
    # options = webdriver.ChromeOptions()
    # Add any ChromeOptions if required
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    driver = webdriver.Chrome()
    driver.get('https://google.com')  # Replace with the actual URL you're testing
    print("Initialization Successful")

    # Additional Statements (Testing)
    driver.quit()
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
