import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import os
import threading
from multiprocessing import Process

def moveon(driver):
    print("Time to move on.")
    driver.quit()

def take_screenshot(URL, timeout, output_file="screenshot1.png"):
    # Validate IP address format
    # Prepare Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for better compatibility
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Set up the Chrome WebDriver
    service = Service("./chromedriver")  # Replace "chromedriver" with the path to your ChromeDriver if necessary
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Construct the URL
        url = f"https://{URL}"
        print(f"Accessing {url}...")

        driver.set_page_load_timeout(timeout)
        # Open the website
        driver.get(url)
        
        # # Wait for the page to load completely
        # driver.implicitly_wait(3)

        # Wait for the page to load completely
        #driver.implicitly_wait(5)

        # Take a screenshot
        screenshot_path = os.path.abspath(output_file)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as: {screenshot_path}")
    
    except Exception as e:
        print(f"An error occurred: ")
    
    finally:
        driver.quit()

def long_running_task():
    while True:
        time.sleep(1)

if __name__ == '__main__':
    common_paths = ["/login", "/app", "/en"]

    for path in common_paths:
        take_screenshot("telegram-ops.com" + path, 5)
    #p = Process(target=long_running_task)
# import re
# words_in_domain = re.split("-", "domain-test") # ("\W+" = .)
# print(words_in_domain)

# print("asd" in "lkjasdmk")