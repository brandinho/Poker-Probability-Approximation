#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 21:33:52 2018

@author: brandinho
"""

import numpy as np
from pokerCombinatorics import calcProbs, findHandStatus

def fetchProbabilityArray(hand, table, currentHandRank):
    """
    the array has the following probabilities:
        [straight flush, four of a kind, full house, flush, straight, three of a kind, two pair, pair]
    """
    
    rankTypes = ["Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"]
    probabilityArray = np.ones(8)
    
    numCardsOnTable = len(table)
    if numCardsOnTable == 0:
        cardsOnTable = "PreFlop"
    elif numCardsOnTable == 3:
        cardsOnTable = "Flop"
    elif numCardsOnTable == 4:
        cardsOnTable = "Turn"
    elif numCardsOnTable == 5:
        cardsOnTable = "River"
        
    handStatus = findHandStatus(hand, table)
    
    if cardsOnTable == "River":
        probabilityArray[:(currentHandRank - 1)] = 0
    else:
        if currentHandRank == 1:
            return probabilityArray
        elif currentHandRank == 2:
            probabilityArray[0] = 0
            return probabilityArray
        elif currentHandRank >= 3:
    
            index = currentHandRank - 1
            tempRankTypes = rankTypes[-(index):]
            for rank in tempRankTypes:
                probabilityArray[(index-1)] = calcProbs(hand, rank, cardsOnTable, handStatus)
                index -= 1

    return probabilityArray

def simulateProbability(hand, table, deck, simulations):
    winner_simulation_counter = 0
    tie_simulation_counter = 0
    probability_array = np.zeros((simulations,2))
    for sim in range(simulations):
        deck.shuffleDeck()
        
        cards_to_remove = list(hand) + table
        clean_shuffled_deck = [x for x in deck.currentDeck if x not in list(cards_to_remove)]
        deck.table = table
        
        theoretical_hands = np.array([list(hand), clean_shuffled_deck[:2]])
        clean_shuffled_deck = clean_shuffled_deck[2:]
        
        deck.table = deck.table + clean_shuffled_deck[:(5-len(table))]
        winner = deck.whoWins(theoretical_hands)[1]
        if winner == 0:
            winner_simulation_counter += 1
        elif winner == None:
            tie_simulation_counter += 1
        probability_array[sim,0] = winner_simulation_counter / (sim + 1)
        probability_array[sim,1] = tie_simulation_counter / (sim + 1)
    return probability_array


def statusDictToInputArray(statusDict, hand_or_table, cards, tableDeck):
    if len(cards) > 0:
        pair_status = 1 if statusDict['Pair'] == True else 0
        if statusDict['straightGap'] == 0:
            straight_gap_status = 1
        elif statusDict['straightGap'] == 1:
            straight_gap_status = 0.8
        elif statusDict['straightGap'] == 2:
            straight_gap_status = 0.6
        elif statusDict['straightGap'] == 3:
            straight_gap_status = 0.4
        elif statusDict['straightGap'] > 3 or statusDict['straightGap'] == -1:
            straight_gap_status = 0.2
            
        NumSplit = []
        for i in range(len(cards)): NumSplit.append(cards[i].split("_"))
        numbersString = np.array(NumSplit)[:,0]    
        handNumbers = list(map(int, numbersString))
        
        if hand_or_table == "Hand":
            suited_status = 1 if statusDict['NumSuited'] == 2 else 0
            card1_status = handNumbers[0] / 14
            card2_status = handNumbers[1] / 14
        if hand_or_table == "Table":
            if statusDict['NumSuited'] > 4:
                suited_status = 1
            elif statusDict['NumSuited'] == 4:
                suited_status = 0.75
            elif statusDict['NumSuited'] == 3:
                suited_status = 0.5
            elif statusDict['NumSuited'] == 2:
                suited_status = 0.25
            elif statusDict['NumSuited'] == 1:
                suited_status = 0
            triple_status = 1 if statusDict['Triple'] == True else 0
            two_pair_status = 1 if statusDict['TwoPair'] == True else 0
            full_house_status = 1 if statusDict['FullHouse'] == True else 0
            runner_runner_status = 1 if statusDict['StraightRunnerRunner'] == True else 0
            single_runner_status = 1 if statusDict['StraightSingleRunner'] == True else 0

            tableDeck.table = cards
            table_rank, _ = tableDeck.evaluateHand([])
            if table_rank == "straight":
                additional_table_status = [1,0,0,0]
            elif table_rank == "flush":
                additional_table_status = [0,1,0,0]
            elif table_rank == "four of a kind":
                additional_table_status = [0,0,1,0]
            elif table_rank == "straight flush":
                additional_table_status = [0,0,0,1]
            else:
                additional_table_status = [0,0,0,0]
        
    else:
        pair_status = 0
        suited_status = 0
        straight_gap_status = 0
        card1_status = 0
        card2_status = 0
        triple_status = 0
        two_pair_status = 0
        full_house_status = 0
        runner_runner_status = 0
        single_runner_status = 0
        additional_table_status = [0,0,0,0]
        
    if hand_or_table == "Hand":
        return np.array([pair_status, suited_status, straight_gap_status, card1_status, card2_status])
    elif hand_or_table == "Table":
        return np.array([pair_status, suited_status, straight_gap_status, 
                         triple_status, two_pair_status, full_house_status, runner_runner_status, 
                         single_runner_status] + additional_table_status)

