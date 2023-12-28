import random
import string
import math
import json

from BlackJack.settings import BASE_DIR

if __name__=='__main__':
    import matplotlib.pyplot as plot
    import numpy as np

def probability_hit(deck, value, sup):
    num_of_cards = 0
    value = sup - value
    for card in deck:
        if type(card) == str:
            card = json.loads(card)
        if type(card) != dict:
            card = card.__dict__
        num_of_cards += 1 if (type(card['value']) == int and card['value'] <= value) else 0
    return num_of_cards/len(deck)
            

def deck_mean(deck):
    mean = 0
    deck_len = len(deck)
    for i in range(1, 11):
        cnt = 0
        for card in deck:
            if type(card) == str:
                card = json.loads(card)
            if type(card) != dict:
                card = card.__dict__
            if card['value'] == i:
                cnt+=1
        mean+= (cnt*i)/deck_len
    return math.ceil(mean)



def probability_advice(deck, dealer, player):
    mean = deck_mean(deck)
    hit = probability_hit(deck, player, 21)
    dealer_win = 1
    while(dealer < min(21, player+mean)):
        prob = (probability_hit(deck, dealer, 21)-probability_hit(deck, dealer, player))
        dealer_win *= prob if prob > 0 else 1
        dealer+=mean
    stay = 1-dealer_win
    return {'hit':hit,'stay': stay}

def beautify(chances):
    chances['hit'] = math.ceil(chances['hit']*100)/100
    chances['stay'] = math.ceil(chances['stay']*100)/100
    return chances

def advice(deck, dealer, player):
    res = {}
    res['prob_rec'] = beautify(probability_advice(deck, dealer, player))
    return res

def generate_game_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    
    