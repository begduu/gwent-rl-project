import json 
import random
import classes

def load_cards(filepath):
    master_card_list = []

    with open(filepath) as file:
        for card in json.load(file):
            if card["type"] == "Weather":
                master_card_list.append(classes.WeatherCard(card["name"], card["ability"]))
            elif card["type"] == "Troop":
                master_card_list.append(classes.TroopCard(card["name"], int(card["Strength"]), card["ability"]))
            elif card["type"] == "Special":
                master_card_list.append(classes.SpecialCard(card["name"], card["ability"]))


def load_prebuild_decks(deck_name, card_list, all_decks_data):
    deck_to_build = {}

    deck_info = 