import numpy as np
from random import randint
from numpyDealer.Card import Card

class Deck:
    # Creates a deck of a standard 52 cards, unshuffled.
    def __init__(self):
        ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
        suits = ("S", "H", "C", "D")

        # Ive doen this like 20 different ways. I dunno why, but this is the only way that works. 
        self.dk = np.array([Card("Joker","Red",-1),Card("Joker", "Black", -1)])
        v = 2
        i = 0
        for s in suits:
            for r in ranks:
                if v == 15:
                    v = 2
                self.dk = np.insert(self.dk, 0, Card(r, s, v))
                i+=1
                v+=1
        self.dk.resize(52)
        self.dk = self.dk.flatten()

    # Returns an iterable version of itself (for loops).
    def __iter__(self):
        return self.dk.flat

    # Returns the card at the "top" of the deck. 
    def deal(self):
        ret = self.dk[0]
        self.removeByIndex(0)
        return ret 

    # Essentially just a search function, but returns and removes value when found
    def dealByRankSuit(self, r, s):
        ret = Card("Joker ", "Red", -1) # Sentry return
        targ = Card(r,s,-2) # Target card with sentry val
        for card in self.dk:
            if card == targ:
                ret = card
                self.removeByCard(ret)
        return ret

    # Returns a random card from the deck
    def dealRand(self):
        m = self.dk.__len__()-1
        g = randint(0,m)
        ret = self.dk[g]
        self.removeByIndex(g)
        return ret

    # Overloads +. Adds the t to the deck at the bottom
    def __add__(self, t):
        if np.iterable(t):
            for add in t:
                self.dk = np.append(self.dk, add)
        else: 
            self.dk = np.append(self.dk, t)
        return self

    # Overloads -. Removes each element of sub, if its iterable. Removes input otherwise.
    def __sub__(self, sub):
        if (np.iterable(sub)):
            for d in self.dk:
                for s in sub:
                    if (d == s):
                        self.removeByCard(d)
        else:
            for d in self.dk:
                if (d == sub):
                    self.removeByCard(sub)
        return self

    # Helper function, eliminates a given card from deck     
    def removeByCard(self, rem:Card):
        dkLength = len(self.dk)
        for i in range(dkLength):
            if(rem == self.dk[i]):
                self.removeByIndex(i)
                break

    # Helper funcion, eliminates a card at given index from deck
    def removeByIndex(self, ind:int):
        while ind < self.dk.__len__()-1:
            self.dk[ind] = self.dk[ind+1]
            ind+=1
        self.dk = np.array(self.dk[0:self.dk.__len__()-1])

    # Prints out every card in deck, in order they were added
    def print(self):
        for i in range(len(self.dk)):
            print(self.dk[i])

    # Prints all cards in deck, in rows by Suit
    def printBySuit(self):
        suits = ("S", "H", "C", "D")
        for s in suits:
            sOut = ""
            for i in range(len(self.dk)):
                if (self.dk[i].suit == s):
                    sOut+=self.dk[i].__str__()+" "
            print(sOut)

    # shuffles the deck
    def shuffle(self):
        i = 52*7
        while i > 0:
            m = self.dk.__len__()-1
            a = randint(0,m)
            b = randint(0,m)
            temp = self.dk[a]
            self.dk[a] = self.dk[b]
            self.dk[b] = temp
            i-=1