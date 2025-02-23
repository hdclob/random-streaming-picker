from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Use your Chrome profile to stay logged in
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument(r"--user-data-dir=D:\Test Chrome Profile\User Data")  
chrome_options.add_argument("--profile-directory=Profile 3")  

# Fix common crash issues
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_episode_ids(show_name, url):
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    # Find all episode elements
    episode_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='set-item']")

    # Extract only valid episode IDs (hrefs starting with "/play")
    episode_ids = [
        el.get_attribute("href").split("/")[-1] 
        for el in episode_elements 
        if el.get_attribute("href") and "/play" in el.get_attribute("href")
    ]

    print(f"Scraped {len(episode_ids)} valid episodes for {show_name}: {episode_ids}")

    return {show_name: episode_ids}

# Scrape multiple shows
shows = {
    "American Dad": "https://www.disneyplus.com/browse/entity-5b4ab988-e3a7-4750-a11a-9aa3d65f8cfe"
}

data = {}
for show, url in shows.items():
    data.update(scrape_episode_ids(show, url))

# Save to JSON
with open("disney_episodes.json", "w") as file:
    json.dump(data, file, indent=2)

print("Saved episode IDs to disney_episodes.json")

driver.quit()
