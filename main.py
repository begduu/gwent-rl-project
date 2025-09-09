import json 
import random
import classes

def load_cards(filepath):
    master_card_list = []

    with open(filepath) as file:
        #TODO change card identifier to "type"
        for card in json.load(file):
            if card["type"] == "weather":
                master_card_list.append(classes.WeatherCard(card["name"], card["ability"]))
            elif card["strength"] != "":
                master_card_list.append(classes.TroopCard(card["name"], int(card["Strength"]), card["ability"]))
            else:
                master_card_list.append(classes.SpecialCard(card["name"], card["ability"]))


def load_prebuild_decks(deck_name, card_list, all_decks_data):
    deck_to_build = {}

    deck_info = 