# Load trauma data from the "traumas/" folder
import json
import os


def load_trauma_data(language="en"):
    traumas = {}
    traumas_folder = "traumas"
    for file in os.listdir(traumas_folder):
        if file.endswith(".json"):
            with open(os.path.join(traumas_folder, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                traumas[file] = {
                    "title": data["title"].get(
                        language, data["title"]["en"]
                    ),  # Default to English if the language is missing
                    "steps": data["steps"],
                }
    return traumas
