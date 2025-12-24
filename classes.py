
from helpers import load_card_data
#import random 
from typing import TypedDict, NotRequired, Any

class CardData(TypedDict):
    name: str
    type: str
    ability: str

    strength: NotRequired[int]
    row: NotRequired[str]

class DeckInfo(TypedDict):
    name: str
    leader_id: str
    card_ids: list[str]

class Card:
    def __init__(self, name: str, ability: str):
        self.name = name
        self.ability = ability

class TroopCard(Card):
    def __init__(self, name: str, ability: str, strength: int, row: str):
        super().__init__(name, ability)
        self.strength = strength 
        self.row = row

class SpecialCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)

class WeatherCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)

class LeaderCard(Card):
    def __init__(self, name, ability):
        super().__init__(name, ability)
        
class Player:
    def __init__(self, faction: str, leader_card: LeaderCard):
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.faction = faction
        self.leader_card = leader_card
        self.num_wins = 0
        self.passed = False

class Board:
    def __init__(self):
        self.p1_close = []
        self.p1_ranged = []
        self.p1_siege = []
        self.p1_close_horn = False
        self.p1_ranged_horn = False
        self.p1_siege_horn = False
        self.p1_score = 0

        self.p2_close = []
        self.p2_ranged = []
        self.p2_siege = []
        self.p2_close_horn = False
        self.p2_ranged_horn = False
        self.p2_siege_horn = False
        self.p2_score = 0

        self.weather = []
      
class GameEngine:
    def __init__(self):
        self.master_card_dict = load_card_data("cards.json")

        self.p1 = None
        self.p2 = None
        self.board = Board()
        self.current_player = None
        self.current_round = 0

    def create_deck(self, 
                    master_card_dict: dict[str, CardData],
                    faction: str, 
                    deck_name: str, 
                    decks_data: dict[str, DeckInfo]
                    ) -> tuple[list[Card], LeaderCard | None] | None:
        """
        Returns a list of card objects and the leader card object
        """
        target_deck_data = None
        leader_card_obj = None
        for deck_info in decks_data.get(faction, []):
            if deck_info.get("name") == deck_name:
                target_deck_data = deck_info
                break

        if not target_deck_data:
            return None

        leader_id = target_deck_data.get("leader_id")
        if leader_id:
            leader_card_data = master_card_dict.get(leader_id)
            if leader_card_data:
                leader_card_obj = LeaderCard(leader_card_data["name"], leader_card_data["ability"])

        card_ids = target_deck_data.get("card_ids", [])
        cards_list: list[Card] = []
        for card_id in card_ids:
            card = master_card_dict.get(card_id)
            if not card:
                continue
            if card["type"] == "Weather":
                cards_list.append(WeatherCard(card["name"], card["ability"]))
            elif card["type"] == "Troop":
                cards_list.append(TroopCard(card["name"], card["ability"], int(card["strength"]), card["row"]))
            elif card["type"] == "Special":
                cards_list.append(SpecialCard(card["name"], card["ability"]))
            else:
                continue
        return cards_list, leader_card_obj

    def get_row_score(self, player: Player, row: str) -> int:
        is_there_weather = False
        row_dict = {
            "close": "Biting Frost",
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
                case "close":
                    row_to_check = self.board.p1_close
                    if self.board.p1_close_horn: is_there_horn = True
                case "ranged":
                    row_to_check = self.board.p1_ranged
                    if self.board.p1_ranged_horn: is_there_horn = True
                case "siege": 
                    row_to_check = self.board.p1_siege
                    if self.board.p1_siege_horn: is_there_horn = True
        if player == self.p2:
            match row:
                case "close":
                    row_to_check = self.board.p2_close
                    if self.board.p2_close_horn: is_there_horn = True
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

        if row_to_check is None:
            return -1
        
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

    def get_player_score(self, player: Player) -> int:
        return (self.get_row_score(player, "close") + 
        self.get_row_score(player, "ranged") + 
        self.get_row_score(player, "siege"))

    def play_card(self, player: Player, card_index: int, row_choice=None) -> bool:
        """
        returns True if it worked else false
        """
        if player != self.current_player:
            return False
        if player.passed:
            return False
        if card_index >= len(player.hand):
            return False
        
        card = player.hand.pop(card_index)


        return True
