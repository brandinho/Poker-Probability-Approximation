#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 21:22:51 2018

@author: brandinho
"""

import math
import numpy as np

def nCr(n, r):
    return (math.factorial(n) / (math.factorial(r) * math.factorial(n - r)))

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))

def countOuts(numbers):
    if 14 in numbers:
        numbers = [1] + numbers
    
    possibilityList= []
    for i in range(len(numbers)):
        possibilityList.append(np.arange(max(numbers[i] - 4, 1), min(numbers[i] + 4, 14) + 1))
    
    straightPossibilityList = []
    for i in range(len(possibilityList)):
        for j in range(len(possibilityList[i]) - 4):
            straightPossibilityList.append(list(possibilityList[i][j:j+5]))
    
    uniquePossibilityList = sort_and_deduplicate(straightPossibilityList)
    
    frequencyCounter = []
    validStraightDraws = []
    missingCards = []
    for i in range(len(uniquePossibilityList)):
        frequencyCounter.append(straightPossibilityList.count(uniquePossibilityList[i]))
        if frequencyCounter[i] >= 3:
            validStraightDraws.append(uniquePossibilityList[i])
            tempMissingCards = list(set(uniquePossibilityList[i]) - set(numbers))
            if len(tempMissingCards) < 3:
                missingCards.append(tempMissingCards)
    
    outs = sort_and_deduplicate(missingCards)
    
    newOuts = list(outs)
    for i in range(len(outs)):
        if len(outs[i]) == 1:
            for j in range(len(outs)):
                if (len(outs[j]) == 2 and outs[i][0] in outs[j] and outs[j] in newOuts or
                    outs[j] == [] and outs[j] in newOuts or
                    len(outs[j]) == 1 and outs[j][0] < min(numbers) and outs[j] in newOuts and [] in outs):
                    newOuts.remove(outs[j])
    
    return newOuts


def calcProbs(hand, rankType, cardsOnTable, handStatus):
    
    FullHouse = handStatus["FullHouse"]
    Triple = handStatus["Triple"]
    TwoPair = handStatus["TwoPair"]
    Pair = handStatus["Pair"]
    NonPair = handStatus["NonPair"]
    
    StraightRunnerRunner = handStatus["StraightRunnerRunner"]
    StraightSingleRunner = handStatus["StraightSingleRunner"]
    
    numSuited = handStatus["NumSuited"]
    
    #I have to calculate the ones below in the hand status function
    straightGap = handStatus["straightGap"]
    straightLowerBound = handStatus["straightLowerBound"]
    straightUpperBound = handStatus["straightUpperBound"]
    
    if cardsOnTable == "PreFlop":
        totalCombinations = nCr(50, 5)
        if rankType == "Pair":
            #We don't have to worry about if we have a pair in our hand because if we did then we wouldn't be calculating this
            probMatchingHand = 6 * nCr(11, 4) * 4**4
            probMatchingTable = 11 * nCr(4, 2) * nCr(10, 3) * 4**3
            marginalProbability1 = probMatchingHand / totalCombinations
            probability = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
        elif rankType == "Two Pair":
            if NonPair == True:
                probMatchingHand = 3**2 * nCr(10, 3) * 4**3
                probMatchingTable = nCr(11, 2) * nCr(4, 2)**2 * 9 * 4
                probMatching_HalfHand_HalfTable = 6 * 11 * nCr(4, 2) * nCr(10, 2) * 4**2
                marginalProbability1 = probMatchingHand / totalCombinations
                marginalProbability2 = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
                probability = marginalProbability2 + (1 - marginalProbability2) * (probMatching_HalfHand_HalfTable / totalCombinations)
            elif Pair == True:
                probability = (12 * nCr(4, 2) * nCr(11, 3) * 4**3) / totalCombinations
        elif rankType == "Three of a Kind":
            if NonPair == True:
                probMatchingHand = 2 * nCr(3, 2) * nCr(11, 3) * 4**3
                probMatchingTable = 11 * nCr(4, 3) * nCr(10, 2) * 4**2
                marginalProbability1 = probMatchingHand / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
            elif Pair == True:
                probability = (2 * nCr(12, 4) * 4**4) / totalCombinations
        elif rankType == "Straight": #I purposely left out the probability of flopping a straight that has nothing to do with your hand
            if straightGap == 0:
                if straightLowerBound > 3 or straightUpperBound < 12:
                    firstMultiplier = 4
                    secondMultiplier = 0
                elif straightLowerBound == 3 or straightUpperBound == 12:
                    firstMultiplier = 3
                    secondMultiplier = 0
                elif straightLowerBound == 2 or straightUpperBound == 13:
                    firstMultiplier = 2
                    secondMultiplier = 0
                elif straightLowerBound == 1 or straightUpperBound == 14:
                    firstMultiplier = 1
                    secondMultiplier = 1
                probBothCardsStraight = (firstMultiplier * 3 * 4**3 * nCr(8, 2) * 4**2) / totalCombinations
                probability = probBothCardsStraight + ((secondMultiplier * 4 * 4**4 * 7 * 4) / totalCombinations) * (1 - probBothCardsStraight)
            elif straightGap == 1:
                if straightLowerBound > 4 or straightUpperBound < 11:
                    firstMultiplier = 3
                    secondMultiplier = 2
                elif straightLowerBound == 4 or straightUpperBound == 11 or straightLowerBound == 3 or straightUpperBound == 12:
                    firstMultiplier = 3
                    secondMultiplier = 1
                elif straightLowerBound == 2 or straightUpperBound == 13:
                    firstMultiplier = 2
                    secondMultiplier = 1
                elif straightLowerBound == 1 or straightUpperBound == 14:
                    firstMultiplier = 1
                    secondMultiplier = 2
                probBothCardsStraight = (firstMultiplier * 3 * 4**3 * nCr(8, 2) * 4**2) / totalCombinations
                probability = probBothCardsStraight + ((secondMultiplier * 4 * 4**4 * 7 * 4) / totalCombinations) * (1 - probBothCardsStraight)
            elif straightGap == 2:
                if straightLowerBound > 4 or straightUpperBound < 11:
                    firstMultiplier = 2
                    secondMultiplier = 4
                elif straightLowerBound == 4 or straightUpperBound == 11:
                    firstMultiplier = 2
                    secondMultiplier = 3
                elif straightLowerBound == 2 or straightUpperBound == 13 or straightLowerBound == 3 or straightUpperBound == 12:
                    firstMultiplier = 2
                    secondMultiplier = 2
                elif straightLowerBound == 1 or straightUpperBound == 14:
                    firstMultiplier = 1
                    secondMultiplier = 3
                probBothCardsStraight = (firstMultiplier * 3 * 4**3 * nCr(8, 2) * 4**2) / totalCombinations
                probability = probBothCardsStraight + ((secondMultiplier * 4 * 4**4 * 7 * 4) / totalCombinations) * (1 - probBothCardsStraight)
            elif straightGap == 3:
                if straightLowerBound > 4 or straightUpperBound < 11:
                    firstMultiplier = 1
                    secondMultiplier = 6
                elif straightLowerBound == 4 or straightUpperBound == 11:
                    firstMultiplier = 1
                    secondMultiplier = 5
                elif straightLowerBound == 3 or straightUpperBound == 12 or straightLowerBound == 1 or straightUpperBound == 14:
                    firstMultiplier = 1
                    secondMultiplier = 4
                elif straightLowerBound == 2 or straightUpperBound == 13:
                    firstMultiplier = 1
                    secondMultiplier = 3
                probBothCardsStraight = (firstMultiplier * 3 * 4**3 * nCr(8, 2) * 4**2) / totalCombinations
                probability = probBothCardsStraight + ((secondMultiplier * 4 * 4**4 * 7 * 4) / totalCombinations) * (1 - probBothCardsStraight)
            elif straightGap > 3:
                multipliers = []
                if straightLowerBound == 1 or straightLowerBound == 2:
                    multipliers.append(2)
                elif straightLowerBound == 3:
                    multipliers.append(3)
                elif straightLowerBound == 4:
                    multipliers.append(4)
                elif (straightLowerBound == 5 or straightLowerBound == 6 or straightLowerBound == 7 or 
                      straightLowerBound == 8 or straightLowerBound == 9):
                    multipliers.append(5)
                if straightUpperBound == 14 or straightUpperBound == 13:
                    multipliers.append(2)
                elif straightUpperBound == 12:
                    multipliers.append(3)
                elif straightUpperBound == 11:
                    multipliers.append(4)
                elif (straightUpperBound == 6 or straightUpperBound == 7 or straightUpperBound == 8 or 
                      straightUpperBound == 9 or straightUpperBound == 10):
                    multipliers.append(5)                    
                firstMultiplier = multipliers[0]
                secondMultiplier = multipliers[1]
                probability = ((firstMultiplier + secondMultiplier) * 4 * 4**4 * 7 * 4) / totalCombinations
            elif straightGap == -1: #This means that they have a pocket pair
                if straightLowerBound > 4 or straightUpperBound < 11:
                    firstMultiplier = 5
                elif straightLowerBound == 4 or straightUpperBound == 11:
                    firstMultiplier = 4
                elif straightLowerBound == 3 or straightUpperBound == 12:
                    firstMultiplier = 3
                elif straightLowerBound == 2 or straightUpperBound == 13 or straightLowerBound == 1 or straightUpperBound == 14:
                    firstMultiplier = 2
                probability = (firstMultiplier * 3 * 4**3 * nCr(8, 2) * 4**2) / totalCombinations             
        elif rankType == "Flush":
            if numSuited == 1: 
                probFlushWithHand = 2 * nCr(12, 4) * 46 #There are 46 remaining cards
                probFlushWithoutHand = 2 * nCr(13, 5)
                marginalProbability1 = probFlushWithHand / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probFlushWithoutHand / totalCombinations)
            elif numSuited == 2:
                probFlushWithHand = nCr(11, 3) * nCr(47, 2)
                probFlushWithoutHand = 3 * nCr(13, 5)
                marginalProbability1 = probFlushWithHand / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probFlushWithoutHand / totalCombinations)
        elif rankType == "Full House":
            if NonPair == True:
                probMatchingHand = 3**2 * nCr(10, 2) * 4**2 #The beginning has 3**2 because both 3C2 and 3C1 are 3
                probMatchingTable = 11 * nCr(4, 3) * 10 * nCr(4, 2)
                probMatching_HandPair_TableTriple = 6 * 11 * nCr(4, 3) * 10 * 4
                probMatching_HandTriple_TablePair = 2 * nCr(3, 2) * 11 * nCr(4, 2) * 10 * 4
                marginalProbability1 = probMatchingHand / totalCombinations
                marginalProbability2 = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
                marginalProbability3 = marginalProbability1 + (1 - marginalProbability1) * (probMatching_HandPair_TableTriple / totalCombinations)
                probability = marginalProbability3 + (1 - marginalProbability3) * (probMatching_HandTriple_TablePair / totalCombinations)                
            elif Pair == True:
                probMatching_HandPair_TableTriple = 12 * nCr(4, 3) * nCr(11, 2) * 4**2
                probMatching_HandTriple_TablePair = 2 * 12 * nCr(4, 2) * nCr(10, 2) * 4**2
                marginalProbability1 = probMatching_HandPair_TableTriple / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probMatching_HandTriple_TablePair / totalCombinations) 
        elif rankType == "Four of a Kind":
            if NonPair == True:
                probMatchingHand = 2 * nCr(11, 2) * 4**2
                probMatchingTable = 11 * 10 * 4
                marginalProbability1 = probMatchingHand / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
            elif Pair == True:
                probability = (nCr(12, 3) * 4**3) / totalCombinations
        elif rankType == "Straight Flush":
            if numSuited == 1 or numSuited == 2 and straightGap > 3: 
                multipliers = []
                if straightLowerBound == 1 or straightLowerBound == 2:
                    multipliers.append(2)
                elif straightLowerBound == 3:
                    multipliers.append(3)
                elif straightLowerBound == 4:
                    multipliers.append(4)
                elif (straightLowerBound == 5 or straightLowerBound == 6 or straightLowerBound == 7 or 
                      straightLowerBound == 8 or straightLowerBound == 9):
                    multipliers.append(5)
                if straightUpperBound == 14 or straightUpperBound == 13:
                    multipliers.append(2)
                elif straightUpperBound == 12:
                    multipliers.append(3)
                elif straightUpperBound == 11:
                    multipliers.append(4)
                elif (straightUpperBound == 6 or straightUpperBound == 7 or straightUpperBound == 8 or 
                      straightUpperBound == 9 or straightUpperBound == 10):
                    multipliers.append(5)   
                if len(multipliers) == 1:
                    multipliers.append(multipliers[0])
                firstMultiplier = multipliers[0]
                secondMultiplier = multipliers[1]
                probability = ((firstMultiplier + secondMultiplier) * 4 * 46) / totalCombinations
            elif numSuited == 2:
                if straightGap == 0:
                    if straightLowerBound > 3 or straightUpperBound < 12:
                        firstMultiplier = 4
                        secondMultiplier = 0
                    elif straightLowerBound == 3 or straightUpperBound == 12:
                        firstMultiplier = 3
                        secondMultiplier = 0
                    elif straightLowerBound == 2 or straightUpperBound == 13:
                        firstMultiplier = 2
                        secondMultiplier = 0
                    elif straightLowerBound == 1 or straightUpperBound == 14:
                        firstMultiplier = 1
                        secondMultiplier = 1
                    probBothCardsStraight = (firstMultiplier * 3 * 47 * 46) / totalCombinations
                    probability = probBothCardsStraight + ((secondMultiplier * 4 * 46) / totalCombinations) * (1 - probBothCardsStraight)
                elif straightGap == 1:
                    if straightLowerBound > 4 or straightUpperBound < 11:
                        firstMultiplier = 3
                        secondMultiplier = 2
                    elif straightLowerBound == 4 or straightUpperBound == 11 or straightLowerBound == 3 or straightUpperBound == 12:
                        firstMultiplier = 3
                        secondMultiplier = 1
                    elif straightLowerBound == 2 or straightUpperBound == 13:
                        firstMultiplier = 2
                        secondMultiplier = 1
                    elif straightLowerBound == 1 or straightUpperBound == 14:
                        firstMultiplier = 1
                        secondMultiplier = 2
                    probBothCardsStraight = (firstMultiplier * 3 * 47 * 46) / totalCombinations
                    probability = probBothCardsStraight + ((secondMultiplier * 4 * 46) / totalCombinations) * (1 - probBothCardsStraight)
                elif straightGap == 2:
                    if straightLowerBound > 4 or straightUpperBound < 11:
                        firstMultiplier = 2
                        secondMultiplier = 4
                    elif straightLowerBound == 4 or straightUpperBound == 11:
                        firstMultiplier = 2
                        secondMultiplier = 3
                    elif straightLowerBound == 2 or straightUpperBound == 13 or straightLowerBound == 3 or straightUpperBound == 12:
                        firstMultiplier = 2
                        secondMultiplier = 2
                    elif straightLowerBound == 1 or straightUpperBound == 14:
                        firstMultiplier = 1
                        secondMultiplier = 3
                    probBothCardsStraight = (firstMultiplier * 3 * 47 * 46) / totalCombinations
                    probability = probBothCardsStraight + ((secondMultiplier * 4 * 46) / totalCombinations) * (1 - probBothCardsStraight)                        
                elif straightGap == 3:
                    if straightLowerBound > 4 or straightUpperBound < 11:
                        firstMultiplier = 1
                        secondMultiplier = 6
                    elif straightLowerBound == 4 or straightUpperBound == 11:
                        firstMultiplier = 1
                        secondMultiplier = 5
                    elif straightLowerBound == 3 or straightUpperBound == 12 or straightLowerBound == 1 or straightUpperBound == 14:
                        firstMultiplier = 1
                        secondMultiplier = 4
                    elif straightLowerBound == 2 or straightUpperBound == 13:
                        firstMultiplier = 1
                        secondMultiplier = 3
                    probBothCardsStraight = (firstMultiplier * 3 * 47 * 46) / totalCombinations
                    probability = probBothCardsStraight + ((secondMultiplier * 4 * 46) / totalCombinations) * (1 - probBothCardsStraight)                        
    elif cardsOnTable == "Flop":
        totalCombinations = nCr(47, 2)
        if rankType == "Pair":
            probMatchingHand = 6 * 8 * 4
            probMatchingTable = 9 * 8 * 4
            probMatchingRunners = 8 * nCr(4, 2)
            marginalProbability1 = probMatchingHand / totalCombinations
            marginalProbability2 = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
            probability = marginalProbability2 + (1 - marginalProbability2) * (probMatchingRunners / totalCombinations)
        elif rankType == "Two Pair":
            if NonPair == True:
                probMatchingHand = 3**2
                probMatchingTable = 3 * 3**2
                probMatching_HalfHand_HalfTable = (2 * 3) * (3 * 3)
                marginalProbability1 = probMatchingHand / totalCombinations
                marginalProbability2 = marginalProbability1 + (1 - marginalProbability1) * (probMatchingTable / totalCombinations)
                probability = marginalProbability2 + (1 - marginalProbability2) * (probMatching_HalfHand_HalfTable / totalCombinations)
            elif Pair == True:
                probability = (3 * 3 * 9 * 4) / totalCombinations
        elif rankType == "Three of a Kind":
            if NonPair == True:
                #We multiply by 5 because there are 5 different cards (2 in your hand and 3 on the flop) that need runner, runner
                probability = (5 * nCr(3, 2)) / totalCombinations
            elif Pair == True:
                probability = (2 * 9 * 4) / totalCombinations
            elif TwoPair == True:
                probability = 0 #Because you would get full house
        elif rankType == "Straight":
            probRunnerRunner = (StraightRunnerRunner * 4**2) / totalCombinations
            
            if NonPair == True:
                probSingleRunner = (StraightSingleRunner * 4 * 8 * 4) / totalCombinations
            elif Pair == True:
                probSingleRunner = (StraightSingleRunner * 4 * 9 * 4) / totalCombinations
            elif TwoPair == True or Triple == True:
                probSingleRunner = 0
                
            probability = probRunnerRunner + (1 - probRunnerRunner) * probSingleRunner
        elif rankType == "Flush":
            if numSuited == 2:
                probability = 0
            elif numSuited == 3:
                probability = nCr(10, 2) / totalCombinations
            elif numSuited == 4:
                probability = (9 * 46) / totalCombinations
        elif rankType == "Full House":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probMatchSetThenPair = 2 * 3 * 3
                probRunnerRunnerSet = 3 * 3
                marginalProbability1 = probMatchSetThenPair / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probRunnerRunnerSet / totalCombinations)
            elif TwoPair == True:
                probMatchHand = 2 * 2 * 10 * 4
                probRunnerRunnerSingle = 3
                marginalProbability1 = probMatchHand / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probRunnerRunnerSingle / totalCombinations)
            elif Triple == True:
                probPairTheBoard = 2 * 3 * 10 * 4
                probRunnerRunner = 10 * nCr(4, 2)
                marginalProbability1 = probPairTheBoard / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probRunnerRunner / totalCombinations)
        elif rankType == "Four of a Kind":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probability = 1 / totalCombinations
            elif TwoPair == True:
                probability = 2 / totalCombinations
            elif Triple == True:
                probability = 10 * 4 / totalCombinations     
            elif FullHouse == True:
                probPairRunnerRunner = 2
                probMatchTriple = 11 * 4
                marginalProbability1 = probPairRunnerRunner / totalCombinations
                probability = marginalProbability1 + (1 - marginalProbability1) * (probMatchTriple / totalCombinations)                
        elif rankType == "Straight Flush":
            probability = 0 #FIX THIS WITH AN ACTUAL PROBABILITY                
    elif cardsOnTable == "Turn":
        totalCombinations = 46
        if rankType == "Pair":
            probability = (6 * 3) / totalCombinations
        elif rankType == "Two Pair":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probability = (4 * 3) / totalCombinations
        elif rankType == "Three of a Kind":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probability = 2 / totalCombinations
            elif TwoPair == True:
                probability = 0 #Because if they get a triple, that would mean a full house
        elif rankType == "Straight":
            probability = (StraightSingleRunner * 4) / totalCombinations
        elif rankType == "Flush":
            if numSuited == 2:
                probability = 0
            elif numSuited == 3:
                probability = 0
            elif numSuited == 4:
                probability = 9 / totalCombinations
        elif rankType == "Full House":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probability = 0
            elif TwoPair == True: #Leaving this for right now, but later I need to check if we have three pair as well
                probability = 4 / totalCombinations
            elif Triple == True:
                probability = (3 * 3) / totalCombinations
        elif rankType == "Four of a Kind":
            if NonPair == True:
                probability = 0
            elif Pair == True:
                probability = 0
            elif TwoPair == True:
                probability = 0
            elif Triple or FullHouse == True:
                probability = 1 / totalCombinations
        elif rankType == "Straight Flush":
            probability = 0 #FIX THIS WITH AN ACTUAL PROBABILITY
    return probability


def findHandStatus(hand, table):
    evaluationHand = list(table)
    evaluationHand.extend(hand)
    
    NonPair = False
    Pair = False
    TwoPair = False
    Triple = False
    FullHouse = False
    
    NumSuitSplit = []
    for i in range(len(evaluationHand)): NumSuitSplit.append(evaluationHand[i].split("_"))
    numbers_string = np.array(NumSuitSplit)[:,0]
    suits = np.array(NumSuitSplit)[:,1]
    
    numbers = list(map(int, numbers_string))
    numbers.sort()
    suits.sort()
    
    pair_sequence = 1
    pair_sequences = []
    pair_values = []
    tempSuited = 1
    NumSuited = 1
    for i in range(1, len(numbers)):
        diff = numbers[i] - numbers[(i-1)]
        
        #Check for pairs
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
            
        #Check for number of suited cards
        if suits[i] == suits[(i-1)]:
            tempSuited += 1
            if tempSuited > NumSuited:
                NumSuited = tempSuited
        elif suits[i] != suits[(i-1)]:
            tempSuited = 1
        
    if len(pair_sequences) > 1 and np.sum(np.array(pair_sequences) == 3) > 0:
        FullHouse = True
    elif len(pair_sequences) == 1 and pair_sequences[0] == 3:
        Triple = True
    elif len(pair_sequences) > 1:
        TwoPair = True
    elif len(pair_sequences) == 1 and pair_sequences[0] == 2:
        Pair = True
    elif len(pair_sequences) == 0:
        NonPair = True
    
    statusDict = {}
    statusDict["NonPair"] = NonPair
    statusDict["Pair"] = Pair
    statusDict["TwoPair"] = TwoPair
    statusDict["Triple"] = Triple
    statusDict["FullHouse"] = FullHouse
    
    outs = countOuts(numbers)
    
    StraightRunnerRunner = 0
    StraightSingleRunner = 0
    for out in outs:
        if len(out) == 1:
            StraightSingleRunner += 1
        elif len(out) == 2:
            StraightRunnerRunner += 1
        
    statusDict["StraightRunnerRunner"] = StraightRunnerRunner
    statusDict["StraightSingleRunner"] = StraightSingleRunner
    
    statusDict["NumSuited"] = NumSuited
    
    NumSuitSplitHand = []
    for i in range(len(hand)): NumSuitSplitHand.append(hand[i].split("_")) 
    hand_numbers_string = np.array(NumSuitSplitHand)[:,0]
    hand_numbers = list(map(int, hand_numbers_string))
    
    statusDict["straightGap"] = abs(hand_numbers[0] - hand_numbers[1]) - 1
    statusDict["straightUpperBound"] = max(hand_numbers)
    statusDict["straightLowerBound"] = min(hand_numbers)    
    
    return statusDict

