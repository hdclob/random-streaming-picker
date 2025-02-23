import json

# Load the JSON file
with open("disney_episodes.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Sort the seasons
sorted_data = {}
for show, seasons in data.items():
    sorted_seasons = dict(sorted(seasons.items(), key=lambda x: int(x[0].split()[-1]) if x[0].split()[-1].isdigit() else float('inf')))
    sorted_data[show] = sorted_seasons

# Save the sorted JSON back to the file
with open("disney_episodes_sorted.json", "w", encoding="utf-8") as file:
    json.dump(sorted_data, file, indent=4)
