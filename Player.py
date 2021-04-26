import math
import requests
import json
from Card import Card, is_valid_move
from Node import Node, tree

URL = "https://unoserver20210412203209.azurewebsites.net/api/"
headers = {'Content-type': 'application/json',
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}


def print_cards(cards):
    for card in cards:
        print(card)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


class Player:
    def __init__(self, name):
        self.name = name
        req = requests.post(URL + 'Match/token', data=json.dumps({"name": name}), headers=headers)
        self.__token = req.json()["token"]
        self.__hand = []
        self.move = False

    def get_token(self):
        return self.__token

    def set_hand(self, hand):
        for card in hand:
            if card is not None:
                self.__hand.append(Card(card))

    def get_hand(self):
        return self.__hand

    def print_hand(self):
        for card in self.__hand:
            print(card)

    def clear_hand(self):
        self.__hand.clear()

    def make_move(self, current_card, current_color, deck):
        root = Node(self.__hand, deck, current_card, None, 0, 0)
        leafs = []
        tree(0, deck, self.__hand, current_card, root, leafs, -math.inf, math.inf)
        candidates = []
        for node in root.children:
            candidates.extend(node.children)
        cards = []
        if len(candidates) > 0:
            cards.append(get_max_estimation_card(candidates))
            self.__hand.remove(cards[0])
            if cards[0].type == 4 or cards[0].type == 5:
                current_color = get_max_valuable_color(self.__hand)
            self.check_identity(cards)
            return [cards, current_color]
        else:
            return [cards, current_color]

    # def make_move(self, current_card, current_color, match_id):
    #     cards = []
    #     number = current_card.number_value
    #     color = current_card.color
    #     if self.check_number(cards, number):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, current_color)
    #         print_cards(cards)
    #         return
    #     if self.check_color(cards, color):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, current_color)
    #         print_cards(cards)
    #         return
    #     if self.check_action(cards):
    #         self.check_identity(cards)
    #         self.send_cards(cards, match_id, random.randint(0, 3))
    #         print_cards(cards)
    #         return
    #     self.send_cards(cards, match_id, current_color)
    #
    # def check_number(self, cards, number):
    #     for card in self.__hand:
    #         if card.number_value == number and card.type == 0:
    #             cards.append(card)
    #             self.__hand.remove(card)
    #             return True
    #     return False
    #
    # def check_color(self, cards, color):
    #     for card in self.__hand:
    #         if card.color == color and card.type != 4 and card.type != 5:
    #             cards.append(card)
    #             self.__hand.remove(card)
    #             return True
    #     return False
    #
    # def check_action(self, cards):
    #     for card in self.__hand:
    #         if card.type == 4 or card.type == 5:
    #             cards.append(card)
    #             self.__hand.remove(card)
    #             return True
    #     return False

    def check_identity(self, cards):
        for card in self.__hand:
            if cards[0] == card:
                cards.append(card)
                self.__hand.remove(card)


def get_max_estimation_card(leafs):
    node = leafs[0]
    for leaf in leafs:
        if leaf.estimation > node.estimation:
            node = leaf
    return node.top


def get_max_valuable_color(hand):
    colors = {0: 0, 1: 0, 2: 0, 3: 0}

    for card in hand:
        colors[card.color] += 1

    values = [colors[0], colors[1], colors[2], colors[3]]
    value = max(values)
    for i in range(len(colors)):
        if value == colors[i]:
            return i
