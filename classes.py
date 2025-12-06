
from helpers import load_card_data
import random 

class Player:
    def __init__(self, deck, hand, faction, leader_card):
        self.deck = deck
        self.hand = hand
        self.discard_pile = []
        self.faction = faction
        self.leader_card = leader_card
        self.num_wins = 0
        self.passed = False

class Board:
    def __init__(self):
        self.p1_melee = []
        self.p1_ranged = []
        self.p1_siege = []
        self.p1_melee_horn = False
        self.p1_ranged_horn = False
        self.p1_siege_horn = False
        self.p1_score = 0

        self.p2_melee = []
        self.p2_ranged = []
        self.p2_siege = []
        self.p2_melee_horn = False
        self.p2_ranged_horn = False
        self.p2_siege_horn = False
        self.p2_score = 0

        self.weather = []

class Card:
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability

class TroopCard(Card):
    def __init__(self, name, strength, ability):
        super().__init__(name, ability)
        self.strength = strength 

class SpecialCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)

class WeatherCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)

class LeaderCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)
        
class Deck():
    def __init__(self):
        self.cards = []
        self.hand = []
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self, num_cards):
        """
        removes and returns a given number of cards from the end of the cards list
        """
        drawn_cards = []
        for _ in range(num_cards):
            if self.cards:
                drawn_cards.append(self.cards.pop())
        return drawn_cards
    
    def create_deck(self, master_card_dict, faction, deck_name, decks_data):

        """
        Adds cards to the deck and returns the LeaderCard object
        """
        target_deck_data = None
        leader_card_obj = None
        for deck_info in decks_data.get(faction, []):
            if deck_info.get("name") == deck_name:
                target_deck_data = deck_info
                break

        if target_deck_data:

            leader_id = target_deck_data.get("leader_id")
            if leader_id:
                leader_card_data = master_card_dict.get(leader_id)
                if leader_card_data:
                    leader_card_obj = LeaderCard(leader_card_data["name"], leader_card_data["ability"])

            card_ids = target_deck_data.get("card_ids", [])

            for card_id in card_ids:
                card = master_card_dict.get(card_id)
                if not card:
                    continue
                if card["type"] == "Weather":
                    self.cards.append(WeatherCard(card["name"], card["ability"]))
                elif card["type"] == "Troop":
                    self.cards.append(TroopCard(card["name"], int(card["Strength"]), card["ability"]))
                elif card["type"] == "Special":
                    self.cards.append(SpecialCard(card["name"], card["ability"]))
                else:
                    continue
        return leader_card_obj
       
class GameEngine:
    def __init__(self):
        self.master_card_dict = load_card_data("cards.json")

        self.p1 = None
        self.p2 = None
        self.board = Board()
        self.current_player = None
        self.current_round = 0

    def get_row_score(self, player: Player, row: str):
        is_there_weather = False
        row_dict = {
            "melee": "Biting Frost",
            "ranged": "Impenetrable Fog",
            "siege": "Torrential Rain"
        }

        target_weather = row_dict[row]
        for weather_card in self.board.weather:
            if weather_card.name == target_weather:
                is_there_weather = True
        
        row_to_check = None
        is_there_horn = False
        if player == self.p1:
            match row:
                case "melee":
                    row_to_check = self.board.p1_melee
                    if self.board.p1_melee_horn: is_there_horn = True
                case "ranged":
                    row_to_check = self.board.p1_ranged
                    if self.board.p1_ranged_horn: is_there_horn = True
                case "siege": 
                    row_to_check = self.board.p1_siege
                    if self.board.p1_siege_horn: is_there_horn = True
        if player == self.p2:
            match row:
                case "melee":
                    row_to_check = self.board.p2_melee
                    if self.board.p2_melee_horn: is_there_horn = True
                case "ranged":
                    row_to_check = self.board.p2_ranged
                    if self.board.p2_ranged_horn: is_there_horn = True
                case "siege": 
                    row_to_check = self.board.p2_siege
                    if self.board.p2_siege_horn: is_there_horn = True

        non_hero_strength = 0
        hero_strength = 0
        morale_giver_count = 0 # How many cards provide a morale boost
        non_hero_card_count = 0 # How many cards are ELIGIBLE to revieve morale boost
        non_hero_morale_giver_count = 0 # How many cards are non-hero and are morale givers
        if row_to_check is not None:
            for card in row_to_check:
                if "morale" in card.ability: morale_giver_count += 1
                if not "hero" in card.ability: non_hero_card_count += 1
                if "morale" in card.ability and not "hero" in card.ability: non_hero_morale_giver_count += 1

                if "horn" in card.ability: is_there_horn = True

                if not "hero" in card.ability and is_there_weather:
                    non_hero_strength += 1
                elif not "hero" in card.ability and not is_there_weather:
                    non_hero_strength += card.strength
                else:
                    hero_strength += card.strength

        morale_bonus = (morale_giver_count * non_hero_card_count) - non_hero_morale_giver_count
        non_hero_strength += morale_bonus
        if is_there_horn:
            non_hero_strength *= 2

        return non_hero_strength + hero_strength

    def get_player_score(self, player):
        total_score = self.get_row_score(player, "melee") + self.get_row_score(player, "ranged") + self.get_row_score(player, "siege")
