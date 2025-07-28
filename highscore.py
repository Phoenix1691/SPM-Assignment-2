import csv
import os

HIGHSCORE_FILE = "highscores.csv"

# Ensure the CSV file exists with headers
def init_highscore_file():
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "score", "mode"])

# Load highscores from CSV
def load_highscores():
    init_highscore_file()
    highscores = []
    with open(HIGHSCORE_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            highscores.append({
                "name": row["name"],
                "score": int(row["score"]),
                "mode": row["mode"]
            })
    return highscores

# Save a new highscore to CSV
def save_highscore(name, score, mode):
    init_highscore_file()
    with open(HIGHSCORE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, score, mode])

# Get top scores by mode
def get_top_scores(mode, limit=10):
    highscores = load_highscores()
    filtered = [s for s in highscores if s["mode"].lower() == mode.lower()]
    sorted_scores = sorted(filtered, key=lambda x: x["score"], reverse=True)
    return sorted_scores[:limit]

