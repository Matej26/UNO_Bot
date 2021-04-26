import math

from Card import is_valid_move


class Node:
    def __init__(self, hand, deck, top, parent, lvl, estimation):
        self.hand = hand
        self.deck = deck
        self.top = top
        self.parent = parent
        self.lvl = lvl
        self.children = []
        self.estimation = estimation

    def set_estimation(self):
        top = self.top
        hand = self.hand

        for card in hand:
            if card.type == 0 and (card.number_value == top.number_value or card.color == top.color):
                self.estimation += 1
            if (card.type == 1 or card.type == 2 or card.type == 3) and \
                    (top.color == card.color or top.type == card.type):
                self.estimation += 2
            if card.type == 4 or card.type == 5:
                self.estimation += 3


def tree(lvl, deck, hand, top, rroot, leafs, alpha, beta):
    if lvl == 5:
        leafs.append(rroot)
        return
    value = -math.inf

    for h in hand:
        if is_valid_move(top, h):
            hhand = hand.copy()
            ddeck = deck.copy()
            hhand.remove(h)
            node = Node(hhand, ddeck, top, rroot, lvl + 1, 0)
            rroot.children.append(node)
            tree(lvl + 1, hhand, ddeck, h, node, leafs, alpha, beta)
            rroot.set_estimation()
            if value <= rroot.estimation:
                value = rroot.estimation
            if lvl % 2 == 0:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
            if beta < alpha:
                break
