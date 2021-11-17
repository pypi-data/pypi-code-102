from typing import NewType
Card = NewType('Card', object)

class Card:
    # Contructor
    def __init__(self, r: str, s: str, v: int): 
        self.rank = r
        self.suit = s
        self.val = v

    # Checks suit of 2 cards
    def suited(self, c):
        if (self.suit == c.suit):
            return True
        else:
            return False
    
    # Overloads == 
    def __eq__(self, oCard):
        if (self.rank == oCard.rank) & (self.suit == oCard.suit):
            return True
        else:
            return False

    # Overloads < 
    def __lt__(self, c):
        if (self.val < c):
            return True
        else:
            return False
    
    # Overloads >
    def __gt__(self, c):
        if (self.val > c):
            return True
        else:
            return False

    # Overloads -
    def __sub__(self, c):
        v = self.val
        vc = c.val
        if self.val == 14:
            if c.val < 8:
                v = 1                
        elif c.val == 14:
            if self.val < 8:
                vc = 1
        return v-vc

    # Returns if called as string
    def __str__(self) -> str:
        return format(self.rank+self.suit)