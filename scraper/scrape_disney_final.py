from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def scrape_all_seasons(show_name, url):
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    show_data = {}

    # Wait for season dropdown button
    try:
        season_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='dropdown-button']"))
        )
        season_dropdown.click()
        time.sleep(2)  # Wait for season list to appear

        # Find all season options
        seasons = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dropdown-list'] li div")

        season_dropdown.click()
        time.sleep(2)  # Wait for season list to disappear

        for season_index in range(len(seasons)):
            # Re-find elements (they might become stale)
            season_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='dropdown-button']"))
            )
            season_dropdown.click()
            time.sleep(2)

            seasons = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='dropdown-list'] li div")

            season_name = seasons[season_index].text.strip()

            print(f"Scraping Season: {season_name}")
            seasons[season_index].click()
            time.sleep(5)  # Wait for episodes to load

            # Scrape episodes for this season
            episodes = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='set-item']")
            episode_ids = [
                el.get_attribute("href").split("/")[-1]
                for el in episodes
                if el.get_attribute("href") and "/play" in el.get_attribute("href")
            ]

            print(f"Found {len(episode_ids)} episodes in {season_name}")

            show_data[season_name] = episode_ids

    except Exception as e:
        print(f"Error scraping {show_name}: {e}")

    return {show_name: show_data}

shows = {
    "Family Guy": "https://www.disneyplus.com/browse/entity-3c3c0f8b-7366-4d15-88ab-18050285978e",
    "Futurama": "https://www.disneyplus.com/browse/entity-85bf4cc1-cd8b-4469-ad87-7289217a0b74",
    "The Simpsons": "https://www.disneyplus.com/browse/entity-cac75c8f-a9e2-4d95-ac73-1cf1cc7b9568",
    "Modern Family": "https://www.disneyplus.com/browse/entity-943f5577-caad-4e34-a8d3-4a9a816d078a",
    "Arrested Development": "https://www.disneyplus.com/browse/entity-92c225ee-2d39-4cb3-a43b-fbcffbefeeb4",
    "Scrubs": "https://www.disneyplus.com/browse/entity-bba197b5-eb03-4a09-b5f6-f04c053471d7",
    "Cleveland Show": "https://www.disneyplus.com/browse/entity-f1bf2db1-d201-4c1f-8b4b-3e8cc79a85f6",
    "Malcolm in the Middle": "https://www.disneyplus.com/browse/entity-ca1ac46e-9883-4125-a6e8-97efce9a2bf5",
}

# JSON file path
json_filename = "disney_episodes.json"

for show, url in shows.items():
    # Scrape data for the current show
    show_data = scrape_all_seasons(show, url)

    # Append scraped data to JSON file
    with open(json_filename, "a") as file:
        json.dump(show_data, file, indent=2)
        file.write("\n")  # Add a newline for readability

    print(f"Saved {show} to {json_filename}")

print("All shows scraped and saved.")
driver.quit()
