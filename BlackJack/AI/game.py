import json
import random

from BlackJack.AI.card import Card, create_deck
from BlackJack.AI.probability import probability_advice
from BlackJack.settings import BASE_DIR

def value_if_not_none(value, alternative):
    return value if value != None else alternative


class Game:
    def __init__(self, files = None, files_lock = None, deck = None, state = None, chain = None):
        self.state = value_if_not_none(state, {
            "dealer" : [],
            "self" : []
        })
        self.chain =  value_if_not_none(chain, {})
        self.deck = value_if_not_none(deck, create_deck())
        self.files = files
        self.files_lock = files_lock

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def make_choice(self, dealer, player):
        res = {}

        content = self.files[BASE_DIR.as_posix()+'/BlackJack/AI/data/root.txt'].read()
        machine = content.count('1')/len(content)

        if random.random() <= machine:
            content = self.files[BASE_DIR.as_posix()+'/BlackJack/AI/data/'+str(dealer) + "_" + str(player)+'.txt'].read()
            n = len(content)
            res['hit'] = content.count('1')/n
            res['stay'] = content.count('0')/n
        else:
            res = probability_advice(self.deck, dealer, player)
 
        return '1' if res['hit'] > res['stay'] else '0'
        
    
    
    def next_round(self, choice = None):

        end_game = False

        if len(self.chain) == 0:
            self.state['dealer'].append(self.deal_card())
            self.state['self'].append(self.deal_card())
            self.state['self'].append(self.deal_card())
            self.chain[BASE_DIR.as_posix()+'/BlackJack/AI/data/root.txt'] = ''
        else:
            dealer = Card.count_value(self.state['dealer'])
            own = Card.count_value(self.state['self'])
            file_name = BASE_DIR.as_posix()+'/BlackJack/AI/data/'+str(dealer) + "_" + str(own)+'.txt'
            if choice == None:
                choice = self.make_choice(dealer, own)
            if choice == '1':
                self.state['self'].append(self.deal_card())
                self.chain[file_name] = int(choice)
            else:
                end_game = True
        current_value = Card.count_value(self.state['self'])
        if current_value >= 21:
            end_game = True
        return end_game
    
    def finish_game(self):

        score = Card.count_value(self.state['self'])

        if score <= 21:
            while Card.count_value(self.state['dealer']) <= 13:
                self.state['dealer'].append(self.deal_card())
        
        dealer_score = Card.count_value(self.state['dealer'])
        won = (score <= 21 and (score > dealer_score or dealer_score > 21 ))
        #print(score, "is my score and ", Card.count_value(self.state['dealer']), "is the dealer's")
        #print(self.chain)
        return won     
    

    def to_json(self):
        res = {}
        res['deck'] = []
        res['dealer'] = []
        res['self'] = []
        res['chain'] = self.chain
        for card in self.deck:
            res['deck'].append((card.to_json() if type(card) != str else card))
        for card in self.state['dealer']:
            res['dealer'].append((card.to_json() if type(card) != str else card))
        for card in self.state['self']:
            res['self'].append((card.to_json() if type(card) != str else card))
        return json.dumps(res)
        