
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
        self.p1_seige = []
        self.p1_score = 0

        self.p2_melee = []
        self.p2_ranged = []
        self.p2_seige = []
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

    #TODO generalize get_row_score to be able to do each row individualy
    def get_row_score(self, player, row):
        strength = 0
        is_there_weather = False
        for weather_card in self.board.weather:
            if weather_card.name == "Biting Frost":
                is_there_weather = True
        for card in self.board.p1_melee:
            if not "hero" in card.ability and is_there_weather:
                strength += card.strength // 2
            else:
                strength += card.strength

    def get_player_score(self, player):
        total_score = 0
        target_rows = []
        if player == self.p1:
            melee
            self.board.p1_melee
    