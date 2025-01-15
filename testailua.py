# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import sys
# import os
# import threading
# from multiprocessing import Process

# def moveon(driver):
#     print("Time to move on.")
#     driver.quit()

# def take_screenshot(ip_address, output_file="screenshot.png"):
#     # Validate IP address format
#     import re
#     ipv4_pattern = r'\b((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b'
#     if not re.match(ipv4_pattern, ip_address):
#         print("Invalid IP address format.")
#         return

#     # Prepare Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run browser in headless mode (no GUI)
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU for better compatibility
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size

#     # Set up the Chrome WebDriver
#     service = Service("./chromedriver")  # Replace "chromedriver" with the path to your ChromeDriver if necessary
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     try:
#         # Construct the URL
#         url = f"http://{ip_address}"
#         print(f"Accessing {url}...")

#         driver.set_page_load_timeout(3)
#         # Open the website
#         driver.get(url)
        
#         print("there0")
#         # # Wait for the page to load completely
#         # driver.implicitly_wait(3)

#         # Wait for the page to load completely
#         #driver.implicitly_wait(5)

#         # Take a screenshot
#         screenshot_path = os.path.abspath(output_file)
#         driver.save_screenshot(screenshot_path)
#         print(f"Screenshot saved as: {screenshot_path}")
    
#     except Exception as e:
#         print(f"An error occurred: ")
    
#     finally:
#         driver.quit()

# def long_running_task():
#     while True:
#         time.sleep(1)

# if __name__ == '__main__':
#     print("here0")
#     p = Process(target=take_screenshot("100.65.191.24"))
#     #p = Process(target=long_running_task)
#     print("here1")
#     p.start()
#     print("here2")
#     p.join(timeout=3)
#     print("here3")
#     if p.is_alive():
#         print("Timeout! Terminating process.")
#         p.terminate()
#         p.join()
import re
words_in_domain = re.split("-", "domain-test") # ("\W+" = .)
print(words_in_domain)

print("asd" in "lkjasdmk")