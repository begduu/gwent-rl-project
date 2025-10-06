import json

def load_card_data(filepath: str) -> dict:
    """Loads the master card data from a JSON file into a dictionary."""
    data_dict = {}
    with open(filepath, "r") as file:
        for card in json.load(file):
            data_dict[card["id"]] = card
    return data_dict

def load_deck_data(filepath: str) -> dict:
    """Loads pre-built deck configurations from a JSON file."""
    with open(filepath, "r") as file:
        return json.load(file)