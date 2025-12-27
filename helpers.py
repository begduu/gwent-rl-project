import json
from classes import Ability

def load_card_data(filepath: str) -> dict[str, dict[str, str]]:
    """
    Loads card data from a JSON file and creates a look up dictionary

    For example a single card would look like this.
    {
        "0": {
            "name": "Mysterious Elf",
            "type": "Troop",
            "id": "0",
            "deck": "neutral",
            "row": "close",
            "strength": "0",
            "ability": "hero spy",
            "filename": "mysterious_elf",
            "count": "1"
        } 
        ...
    }

    Args:
        filepath (str): path to the JSON file containing the card information

    Returns:
        dict[str, dict[str, str]]: Dictionary where the keys are the card ids
        and the values are dictionaries containing the card attributes (AS STRINGS)
    """
    data_dict: dict[str, dict[str, str]] = {}
    with open(filepath, "r") as file:
        for card in json.load(file):
            data_dict[card["id"]] = card
    return data_dict

def load_deck_data(filepath: str) -> dict:
    """Loads pre-built deck configurations from a JSON file."""
    with open(filepath, "r") as file:
        return json.load(file)

def parse_abilities(abilities_str: str) -> list[Ability]:
    """
    Splits abilities apart as some abilities are 
    written as 'hero mardroeme' which are two seperate abilities.
    One being 'hero' and the other being 'mardroeme'

    Args:
        abilities_str (str): String of abilities

    Returns:
        list[Ability]: A list of abilities of type Ability
    """
    if not abilities_str or abilities_str == "":
        return []
    
    abilities_list = abilities_str.split()

    return [Ability(ability) for ability in abilities_list]