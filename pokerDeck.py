#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 23:32:10 2018

@author: brandinho
"""

import numpy as np

class pokerDeck():
    def __init__(self):
        self.currentDeck = {}
        self.table = []
        
        ### 11 is Jack, 12 is Queen, and 13 is King, 14 is Ace ###
        
        self.cards = np.array(["2_S", "3_S", "4_S", "5_S", "6_S", "7_S", "8_S", "9_S", "10_S", "11_S", "12_S", "13_S", "14_S",
                               "2_H", "3_H", "4_H", "5_H", "6_H", "7_H", "8_H", "9_H", "10_H", "11_H", "12_H", "13_H", "14_H",
                               "2_C", "3_C", "4_C", "5_C", "6_C", "7_C", "8_C", "9_C", "10_C", "11_C", "12_C", "13_C", "14_C",
                               "2_D", "3_D", "4_D", "5_D", "6_D", "7_D", "8_D", "9_D", "10_D", "11_D", "12_D", "13_D", "14_D"])
        
        ### I am only making it heads up for now ###
        
        self.players = 2
        
    ### Call this method to shuffle the deck between hands ###
    
    def shuffleDeck(self):
        self.table = []
        self.currentDeck = list(self.cards)
        np.random.shuffle(self.currentDeck)
        
    ### Call this method to deal the hole cards for the players in the game ###
    
    def dealCards(self):
        tableHands = np.empty([self.players, 2], dtype = '<U4')
        for i in range(self.players):
            for j in range(2):
                tableHands[i, j] = self.currentDeck[0]
                self.currentDeck.pop(0)
        return tableHands
    
    ### Call this method to flip the Flop cards ###
    
    def flipFlop(self):
        self.currentDeck.pop(0) #Burn the first card
        self.table.extend(self.currentDeck[:3])
        for i in range(3): self.currentDeck.pop(0)
    
    ### Call this method to flip the Turn card ###
    
    def flipTurn(self):
        self.currentDeck.pop(0)
        self.table.append(self.currentDeck[0])
        self.currentDeck.pop(0)
    
    ### Call this method to flip the River card ###
    
    def flipRiver(self):
        self.currentDeck.pop(0)
        self.table.append(self.currentDeck[0])
        self.currentDeck.pop(0)
    
    ### Naive implementation of a hand evaluation ###
    
    def evaluateHand(self, hand):
        
        ### Start by evaluating the top hands and then work my way down ###
        
        evaluationHand = list(self.table)
        evaluationHand.extend(hand)
        
        NumSuitSplit = []
        for i in range(len(evaluationHand)): NumSuitSplit.append(evaluationHand[i].split("_"))
        numbers_string = np.array(NumSuitSplit)[:,0]
        suits = np.array(NumSuitSplit)[:,1]
        
        numbers = list(map(int, numbers_string))
        numbers.sort()
        suits.sort()
        
        cardsArray = np.array(NumSuitSplit)
        heartsArray = cardsArray[cardsArray[:,1] == 'H', ]
        spadesArray = cardsArray[cardsArray[:,1] == 'S', ]
        clubsArray = cardsArray[cardsArray[:,1] == 'C', ]
        diamondsArray = cardsArray[cardsArray[:,1] == 'D', ]
        
        ### We check to see if we have a straight flush ###
        
        straight_flush_sequence = 1
        flush_sequence = 1
        flush_status = False
        straight_sequence = 1
        straight_status = False
        pair_sequence = 1
        pair_sequences = []
        pair_values = []
        for i in range(1, len(numbers)):
            diff = numbers[i] - numbers[(i-1)]
            
            ### Check for straight flush ###
            
            if len(heartsArray) >= 5 and i < len(heartsArray):
                hearts_numbers_string = heartsArray[:,0]
                hearts_numbers = list(map(int, hearts_numbers_string))
                hearts_numbers.sort()
                
                hearts_diff = hearts_numbers[i] - hearts_numbers[(i-1)]
                if hearts_diff == 1:
                    straight_flush_sequence += 1
                    high_card = numbers[i]
                elif hearts_diff > 1 and straight_flush_sequence < 5:
                    straight_flush_sequence = 1
            elif len(spadesArray) >= 5 and i < len(spadesArray):
                spades_numbers_string = spadesArray[:,0]
                spades_numbers = list(map(int, spades_numbers_string))
                spades_numbers.sort()
                
                spades_diff = spades_numbers[i] - spades_numbers[(i-1)]
                if spades_diff == 1:
                    straight_flush_sequence += 1
                    high_card = numbers[i]
                elif spades_diff > 1 and straight_flush_sequence < 5:
                    straight_flush_sequence = 1
            elif len(clubsArray) >= 5 and i < len(clubsArray): 
                clubs_numbers_string = clubsArray[:,0]
                clubs_numbers = list(map(int, clubs_numbers_string))
                clubs_numbers.sort()
                
                clubs_diff = clubs_numbers[i] - clubs_numbers[(i-1)]
                if clubs_diff == 1:
                    straight_flush_sequence += 1
                    high_card = numbers[i]
                elif clubs_diff > 1 and straight_flush_sequence < 5:
                    straight_flush_sequence = 1
            elif len(diamondsArray) >= 5 and i < len(diamondsArray):
                diamonds_numbers_string = diamondsArray[:,0]
                diamonds_numbers = list(map(int, diamonds_numbers_string))
                diamonds_numbers.sort()
                
                diamonds_diff = diamonds_numbers[i] - diamonds_numbers[(i-1)]
                if diamonds_diff == 1:
                    straight_flush_sequence += 1
                    high_card = numbers[i]
                elif diamonds_diff > 1 and straight_flush_sequence < 5:
                    straight_flush_sequence = 1
                
            ### Check for flush ###
            
            if suits[i] == suits[(i-1)] and flush_status == False:
                flush_sequence += 1
                final_suit = suits[i]
            else:
                if flush_sequence < 5:
                    flush_sequence = 1
                else:
                    flush_status = True
                
            ### Check for straight ###
            
            if diff == 1 and straight_status == False:
                straight_sequence += 1
                high_card = numbers[i]
            elif diff > 1:
                if straight_sequence < 5:
                    straight_sequence = 1
                else:
                    straight_status = True

            ### Check for pairs ###
            
            if diff == 0:
                pair_sequence += 1
                pair = numbers[i]
                if i == len(numbers) - 1:
                    pair_values.append(pair)
                    pair_sequences.append(pair_sequence)
            else:
                if pair_sequence > 1:
                    pair_values.append(pair)
                    pair_sequences.append(pair_sequence)
                pair_sequence = 1
                
        if straight_flush_sequence < 5 and len(heartsArray) >= 5:
            if len(list(filter(lambda x: x in [2,3,4,5], list(set(hearts_numbers))))) == 4:
                if 14 in hearts_numbers:
                    straight_flush_sequence = 5
                    top5cards = [1,2,3,4,5]
        elif straight_flush_sequence < 5 and len(spadesArray) >= 5:
            if len(list(filter(lambda x: x in [2,3,4,5], list(set(spades_numbers))))) == 4:
                if 14 in spades_numbers:
                    straight_flush_sequence = 5
                    top5cards = [1,2,3,4,5]
        elif straight_flush_sequence < 5 and len(clubsArray) >= 5:
            if len(list(filter(lambda x: x in [2,3,4,5], list(set(clubs_numbers))))) == 4:
                if 14 in clubs_numbers:
                    straight_flush_sequence = 5
                    top5cards = [1,2,3,4,5]
        elif straight_flush_sequence < 5 and len(diamondsArray) >= 5:
            if len(list(filter(lambda x: x in [2,3,4,5], list(set(diamonds_numbers))))) == 4:
                if 14 in diamonds_numbers:
                    straight_flush_sequence = 5
                    top5cards = [1,2,3,4,5]
        
        non_pairs = np.setdiff1d(numbers, pair_values)

        if straight_flush_sequence >= 5:
            hand_description = "straight flush"
            top5cards = list(range(high_card + 1 - 5, high_card + 1))
        elif (len(pair_sequences) == 1 and pair_sequences[0] == 4) or (len(pair_sequences) > 1 and np.sum(np.array(pair_sequences) == 4) > 0):
            hand_description = "four of a kind"
            if len(non_pairs) > 0:
                top5cards = [non_pairs[-1]] + [pair_values[0]]*4
            else:
                top5cards = [max(sum((np.array(pair_sequences) != 4) * pair_values), non_pairs)] + [sum((np.array(pair_sequences) == 4) * pair_values)]*4
        elif len(pair_sequences) > 1 and np.sum(np.array(pair_sequences) == 3) > 0:
            hand_description = "full house"
            triple_index = sum((np.array(pair_sequences) == 3) * list(range(len(pair_sequences))))
            top5cards = [np.delete(pair_values, triple_index)[-1]]*2 + [pair_values[triple_index]]*3
        elif flush_sequence >= 5:
            hand_description = "flush"
            if final_suit == "H":
                hearts_numbers_string = heartsArray[:,0]
                hearts_numbers = list(map(int, hearts_numbers_string))
                hearts_numbers.sort()
                top5cards = hearts_numbers[-5:]
            elif final_suit == "S":
                spades_numbers_string = spadesArray[:,0]
                spades_numbers = list(map(int, spades_numbers_string))
                spades_numbers.sort()
                top5cards = spades_numbers[-5:]
            elif final_suit == "C":
                clubs_numbers_string = clubsArray[:,0]
                clubs_numbers = list(map(int, clubs_numbers_string))
                clubs_numbers.sort()
                top5cards = clubs_numbers[-5:]
            elif final_suit == "D":
                diamonds_numbers_string = diamondsArray[:,0]
                diamonds_numbers = list(map(int, diamonds_numbers_string))
                diamonds_numbers.sort()
                top5cards = diamonds_numbers[-5:]
            
        elif straight_sequence >= 5:
            hand_description = "straight" 
            top5cards = list(range(high_card + 1 - 5, high_card + 1))
        elif len(list(filter(lambda x: x in [2,3,4,5], list(set(numbers))))) == 4:
            if 14 in numbers:
                hand_description = "straight"
                top5cards = [1,2,3,4,5]
            else:                
                if len(pair_sequences) == 1 and pair_sequences[0] == 3:
                    hand_description = "three of a kind"
                    top5cards = list(non_pairs[-2:]) + [pair_values[0]]*3
                elif len(pair_sequences) > 1:
                    hand_description = "two pairs"
                    top5cards = list(non_pairs[-1:]) + [pair_values[-2]]*2 + [pair_values[-1]]*2
                elif len(pair_sequences) == 1 and pair_sequences[0] == 2:
                    hand_description = "pair"
                    top5cards = list(non_pairs[-3:]) + [pair_values[0]]*2
                elif len(pair_sequences) == 0:
                    hand_description = "high card"
                    top5cards = list(non_pairs[-5:])
        elif len(pair_sequences) == 1 and pair_sequences[0] == 3:
            hand_description = "three of a kind"
            top5cards = list(non_pairs[-2:]) + [pair_values[0]]*3
        elif len(pair_sequences) > 1:
            hand_description = "two pairs"
            if len(pair_sequences) == 3:
                top5cards = [pair_values[-3]] + [pair_values[-2]]*2 + [pair_values[-1]]*2
            else:
                top5cards = list(non_pairs[-1:]) + [pair_values[-2]]*2 + [pair_values[-1]]*2
        elif len(pair_sequences) == 1 and pair_sequences[0] == 2:
            hand_description = "pair"
            top5cards = list(non_pairs[-3:]) + [pair_values[0]]*2
        elif len(pair_sequences) == 0:
            hand_description = "high card"
            top5cards = list(non_pairs[-5:])
        
        return hand_description, top5cards
    
    ### Call this method to get a numerical ranking from the hand evaluation ###
    
    def handRanking(self, description):
        if description == "straight flush":
            ranking = 1
        elif description == "four of a kind":
            ranking = 2
        elif description == "full house":
            ranking = 3
        elif description == "flush":
            ranking = 4
        elif description == "straight":
            ranking = 5
        elif description == "three of a kind":
            ranking = 6
        elif description == "two pairs":
            ranking = 7
        elif description == "pair":
            ranking = 8
        elif description == "high card":
            ranking = 9
        return ranking
    
    ### Call this method if both players have the same hand rank to break the tie ###
    
    def breakTie(self, top5cards_array):
        
        ### This method currently only supports heads up ###
        
        for i in range(5):
            winner = np.argwhere(top5cards_array[:,-(i+1)] == np.amax(top5cards_array[:,-(i+1)])).flatten()
            if winner.shape[0] == 1:
                return winner[0]
        return None
    
    ### Call this method to see who wins the hand ###
    
    def whoWins(self, hands):
        previousRanking = 10 # 10 is out of the range, so the first hand will always be better
        for i in range(hands.shape[0]):
            currentHand, tempBestCards = self.evaluateHand(hands[i,])
            currentRanking = self.handRanking(currentHand)
            if i == 0:
                bestCards = tempBestCards
            else:
                bestCards = np.vstack((bestCards, tempBestCards))
            if currentRanking < previousRanking:
                bestHand = currentHand
                bestHandPlayer = i
                status = "winner"
                previousRanking = currentRanking
            elif currentRanking == previousRanking:
                bestHand = currentHand
                status = "tie"
                previousRanking = currentRanking
        if status == "tie":
            bestHandPlayer = self.breakTie(bestCards)
            if bestHandPlayer == None:
                winningDescription = "The result ended in a tie with a {} \nTop 5 cards were {}".format(bestHand, bestCards)
                return winningDescription, bestHandPlayer
            else:
                winningDescription = "Player {} won the hand with a {} \nTop 5 cards were {}".format(bestHandPlayer, bestHand, bestCards)
                return winningDescription, bestHandPlayer
        else:
            winningDescription = "Player {} won the hand with a {} \nTop 5 cards were {}".format(bestHandPlayer, bestHand, bestCards)
            return winningDescription, bestHandPlayer