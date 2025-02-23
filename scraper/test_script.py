from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome Options
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument(r"--user-data-dir=D:\Test Chrome Profile\User Data")  
chrome_options.add_argument("--profile-directory=Profile 3")  # Try another profile

chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open a test page
driver.get("https://www.google.com")
time.sleep(3)
print("Chrome launched successfully!")

driver.quit()
