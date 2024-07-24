import json


# Load and save functions
def load_prompts(filename="prompts.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_prompts(prompts, filename="prompts.json"):
    with open(filename, "w") as file:
        json.dump(prompts, file, indent=4)
