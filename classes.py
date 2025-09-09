import json
class Player:
    def __init__(self, deck, hand, faction, leader_card):
        self.deck = deck
        self.hand = hand
        self.discard_pile = []
        self.faction = faction
        self.leader_card = leader_card
        self.hp = 2

class Board:
    def __init__(self):
        self.p1_melee = []
        self.p1_ranged = []
        self.p1_seige = []

        self.p2_melee = []
        self.p2_ranged = []
        self.p2_seige = []

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

class Deck:
    def __init__(self):
        self.cards = []

    def 
   

class GameEngine:
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.board = Board()
        self.current_player = None
        self.current_round = 0
    
    