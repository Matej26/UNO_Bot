import enum


class Type(enum.Enum):
    Numeric = 0
    Reverse = 1
    Skip = 2
    Take_two = 3
    Take_four_and_choose_color = 4
    Choose_color = 5


class Color(enum.Enum):
    Red = 0
    Green = 1
    Blue = 2
    Yellow = 3


def is_valid_move(top, card):
    if top.color == card.color:
        return True
    if (top.type == 0 and card.type == 0) and \
            (top.number_value == card.number_value):
        return True
    if (top.type == 2 or top.type == 3 or top.type == 1) and \
            top.type == card.type:
        return True
    if card.type == 4 or card.type == 5:
        return True


class Card:
    def __init__(self, card):
        self.type = card['type']
        self.number_value = card['numberValue']
        self.color = card['color']

    def __str__(self):
        if self.type == 0:
            return str(Color(self.color).name) + " " + str(self.number_value)
        else:
            return str(Color(self.color).name) + " " + str(Type(self.type).name)

    def to_json(self):
        return {"type": self.type, "numberValue": self.number_value, "color": self.color}

    def __eq__(self, other):
        return self.type == other.type and \
               self.number_value == other.number_value and \
               self.color == other.color
