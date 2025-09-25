import json

card_database = "cards.json"
prebuilt_decks = "decks.json"

def load_card_data(filepath):
    data_map= {}

    with open(filepath, "r") as file:
        for card in json.load(file):
            data_map[card["id"]] = card

    return data_map

if __name__ == "__main__":
    master_card_map = load_card_data(card_database)

    with open(prebuilt_decks, "r") as file:
        all_decks_map = json.load(file)

    for faction_key, deck_list in all_decks_map.items():
        print(faction_key)
        
        for deck_object in deck_list:
            deck_name = deck_object["name"]
            card_ids = deck_object["card_ids"]
            is_deck_valid = True

            num_valid_cards = 0
            total_cards_in_deck = len(card_ids)

            print(f"    Testing deck: {deck_name}")

            for card_id in card_ids:
                card_data = master_card_map.get(card_id)

                if card_data:
                    card_name = card_data["name"]
                    card_faction = card_data["deck"]

                    is_faction_match = (
                        card_faction == faction_key or
                        card_faction == "neutral" or
                        card_faction == "special" or
                        card_faction == "weather"
                        )
                    if is_faction_match:
                        print(f"        All good: {card_name}")
                        num_valid_cards += 1
                    else:
                        print(f"        {card_name} ({card_faction}) is not allowed in a {faction_key} deck")
                        is_deck_valid = False

            print(f"    {num_valid_cards} / {total_cards_in_deck} cardshave valid factions")
            if is_deck_valid:
                print(f"    {deck_name} is valid")
            else:
                print(f"    {deck_name} is invalid")

    print("Deck validation complete")