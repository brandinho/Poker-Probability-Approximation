#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 21:33:52 2018

@author: brandinho
"""

import math
import numpy as np

"Probability Function Below (Not Considering what opponent has in their hand)" 

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

import random
import tensorflow as tf

# Create sample data to train on
#sampleDeck = pokerDeck()
#sampleHands = []
#tableCardsOptions = [0, 3, 4, 5]
#sampleTableCards = []
#num_data_points = 150000
#for i in range(num_data_points):
#    sampleDeck.shuffleDeck()
#    
#    sampleHands.append(sampleDeck.currentDeck[:2])
#    cleanDeck = sampleDeck.currentDeck[2:]
#    
#    sampleTableCards.append(cleanDeck[:random.choice(tableCardsOptions)])
#    
#    
#
#simulationDeck = pokerDeck()
#evaluationDeck = pokerDeck()
#tableEvaluationDeck = pokerDeck()
#mock_array = ['prob1', 'prob2', 'prob3', 'prob4', 'prob5', 'prob6', 'prob7', 'prob8', 
#              'pairStatusHand', 'suitedStatusHand', 'straightGapStatusHand', 'lowCardHand', 'highCardHand',
#              'pairStatusTable', 'suitedStatusTable', 'straightGapStatusTable', 'tripleStatusTable', 'TwoPairStatusTable', 
#              'FullHouseStatusTable', 'RunnerRunnerStatusTable', 'SingleRunnerStatusTable', 
#              'Straight - Table', 'Flush - Table', 'Four of a Kind - Table', 'Straight Flush - Table',
#              'preflopOneHot', 'flopOneHot', 'turnOneHot', 'riverOneHot']
#
#probabilityInputList = np.zeros((len(sampleHands), len(mock_array)))
#probabilityList = np.zeros((len(sampleHands),2))
##probabilityList_1000 = np.zeros((len(sampleHands),2))
##probabilityList_10000 = np.zeros((len(sampleHands),2))
#for j in range(len(sampleHands)):
#    
#    if j % 1000 == 0:
#        print('You are at iteration {}'.format(j))
#    
#    evaluationDeck.shuffleDeck(); evaluationDeck.table = sampleTableCards[j]
#    sampleCurrentHand, sampleTempBestCards = evaluationDeck.evaluateHand(sampleHands[j])
#    sampleCurrentRanking = simulationDeck.handRanking(sampleCurrentHand)
#    probArray = fetchProbabilityArray(sampleHands[j], sampleTableCards[j], sampleCurrentRanking)
#    
#    # I want to get my status irrespective of the table cards (because those are shared)
#    preflopStatusDict = findHandStatus(sampleHands[j], [])
#    statusArray = statusDictToInputArray(preflopStatusDict, "Hand", sampleHands[j], None)
#    if len(sampleTableCards[j]) != 0:
#        tableStatusDict = findHandStatus(sampleTableCards[j], [])
#    else:
#        tableStatusDict = {}
#    tableStatusArray = statusDictToInputArray(tableStatusDict, "Table", sampleTableCards[j], tableEvaluationDeck)
#    
#    if len(sampleTableCards[j]) == 0:
#        tableStatus = [1,0,0,0]
#    elif len(sampleTableCards[j]) == 3:
#        tableStatus = [0,1,0,0]
#    elif len(sampleTableCards[j]) == 4:
#        tableStatus = [0,0,1,0]
#    elif len(sampleTableCards[j]) == 5:
#        tableStatus = [0,0,0,1]
#        
#    probabilityInputList[j,] = np.concatenate((probArray, statusArray, tableStatusArray, tableStatus))
#    temp_prob_array = simulateProbability(sampleHands[j], sampleTableCards[j], simulationDeck, 1000)
#        
#    probabilityList[j,] = temp_prob_array[-1,]


#prob_array_1000 = temp_prob_array
#prob_array_100000 = temp_prob_array


def rolling_std(series, rolling_window):
    new_series = np.zeros(series.shape)
    for i in range(rolling_window - 1, new_series.shape[0]):
        new_series[i] = np.std(series[i-rolling_window+1:i+1])
    return new_series

def replace_string_with_suits(cards):
    new_cards = ''
    if len(cards) > 0:
        NumSuitSplit = []
        for i in range(len(cards)): NumSuitSplit.append(cards[i].split("_"))
        numbers_string = np.array(NumSuitSplit)[:,0]
        suits = np.array(NumSuitSplit)[:,1]
            
        for s in range(suits.shape[0]):
            if suits[s] == 'S':
                new_cards += ' ' + numbers_string[s] + '♠'
            elif suits[s] == 'C':
                new_cards += ' ' + numbers_string[s] + '♣'
            elif suits[s] == 'D':
                new_cards += ' ' + numbers_string[s] + '♦'
            elif suits[s] == 'H':
                new_cards += ' ' + numbers_string[s] + '♥'
    else:
        new_cards = ' Nothing'

    return new_cards


import plotly
import plotly.graph_objs as go
    
n_simulations = 1000
n_iterations = 25

#3, 2, 6, 0
example_index = 8
example_1_simulation_array = np.zeros((n_simulations, n_iterations))
for n in range(n_iterations):
    example_1_simulation_array[:,n] = simulateProbability(sampleHands[example_index], sampleTableCards[example_index], simulationDeck, n_simulations)[:,0]
example_1_true_probability = simulateProbability(sampleHands[example_index], sampleTableCards[example_index], simulationDeck, 100000)[:,0]
example_1_hand = 'Hand:' + replace_string_with_suits(sampleHands[example_index])
example_1_table = 'Table:' + replace_string_with_suits(sampleTableCards[example_index])

#preflop_deviation1 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#preflop_deviation2 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#flop_deviation1 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#flop_deviation2 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#flop_deviation3 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#turn_deviation1 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#turn_deviation2 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#river_deviation1 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#river_deviation2 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])
#river_deviation3 = np.max(example_1_simulation_array[-1,]) - np.min(example_1_simulation_array[-1,])


example_2_simulation_array = np.zeros((n_simulations, n_iterations))
for n in range(n_iterations):
    example_2_simulation_array[:,n] = simulateProbability(sampleHands[1], sampleTableCards[1], simulationDeck, n_simulations)[:,0]
example_2_true_probability = simulateProbability(sampleHands[1], sampleTableCards[1], simulationDeck, 100000)[:,0]
example_2_hand = 'Hand:' + replace_string_with_suits(sampleHands[1])
example_2_table = 'Table:' + replace_string_with_suits(sampleTableCards[1])

example_3_simulation_array = np.zeros((n_simulations, n_iterations))
for n in range(n_iterations):
    example_3_simulation_array[:,n] = simulateProbability(sampleHands[2], sampleTableCards[2], simulationDeck, n_simulations)[:,0]
example_3_true_probability = simulateProbability(sampleHands[2], sampleTableCards[2], simulationDeck, 100000)[:,0]
example_3_hand = 'Hand:' + replace_string_with_suits(sampleHands[2])
example_3_table = 'Table:' + replace_string_with_suits(sampleTableCards[2])

example_4_simulation_array = np.zeros((n_simulations, n_iterations))
for n in range(n_iterations):
    example_4_simulation_array[:,n] = simulateProbability(sampleHands[9], sampleTableCards[9], simulationDeck, n_simulations)[:,0]
example_4_true_probability = simulateProbability(sampleHands[9], sampleTableCards[9], simulationDeck, 100000)[:,0]
example_4_hand = 'Hand:' + replace_string_with_suits(sampleHands[9])
example_4_table = 'Table:' + replace_string_with_suits(sampleTableCards[9])

### Below we are plotting the probabities as we make more simulations (as we increase N we see it converge)

trace0_bottom = go.Scatter(
    y = np.min(example_1_simulation_array, axis = 1),
    fill= None,
    mode='lines',
    line=dict(width = 0,
    ),
    showlegend = False
)
trace0_top = go.Scatter(
    y = np.max(example_1_simulation_array, axis = 1),
        fill= 'tonexty',
    mode='lines',
    line=dict(width = 0,
        color='rgb(102, 204, 0)',
    ),
    showlegend = False
)
trace0_line = go.Scatter(
    y = np.median(example_1_simulation_array, axis = 1),
    line = dict(color = 'rgb(0, 153, 0)',),
    name = example_1_hand + '   ' + example_1_table
)

trace1_bottom = go.Scatter(
    y = np.min(example_2_simulation_array, axis = 1),
    fill= None,
    mode='lines',
    line=dict(width = 0,
    ),
    showlegend = False
)
trace1_top = go.Scatter(
    y = np.max(example_2_simulation_array, axis = 1),
        fill= 'tonexty',
    mode='lines',
    line=dict(width = 0,
        color='rgb(153, 204, 255)',
    ),
    showlegend = False
)
trace1_line = go.Scatter(
    y = np.median(example_2_simulation_array, axis = 1),
    line = dict(color = 'rgb(51, 51, 255)',),
    name = example_2_hand + '   ' + example_2_table
)

trace2_bottom = go.Scatter(
    y = np.min(example_3_simulation_array, axis = 1),
    fill= None,
    mode='lines',
    line=dict(width = 0,
    ),
    showlegend = False
)
trace2_top = go.Scatter(
    y = np.max(example_3_simulation_array, axis = 1),
        fill= 'tonexty',
    mode='lines',
    line=dict(width = 0,
        color='rgb(255, 102, 102)',
    ),
    showlegend = False
)
trace2_line = go.Scatter(
    y = np.median(example_3_simulation_array, axis = 1),
    line = dict(color = 'rgb(255, 0, 0)',),
    name = example_3_hand + '   ' + example_3_table
)


layout = {
    'showlegend': True,
    'legend': dict(orientation = "h"),
    'title': "Stable Probability Approximation",
    'yaxis': dict(title = "Probability of Winning")
}

fig = fig = {
    'data': [trace0_bottom, trace0_top, trace0_line, 
             trace1_bottom, trace1_top, trace1_line,
             trace2_bottom, trace2_top, trace2_line],
    'layout': layout,
}

plotly.offline.plot(fig)


# Below we display bar charts with error bars 

trace1 = go.Scatter(
    x=['Green Scenario', 'Blue Scenario', 'Red Scenario'],
    y=[np.median(example_1_simulation_array[-1:,]), np.median(example_2_simulation_array[-1:,]), np.median(example_3_simulation_array[-1:,])],
    name='Approximated Probability Ranges',
    mode = 'lines',
#    marker = dict(color = 'rgba(204,204,204,1)'),
    error_y=dict(
        type='data',
        symmetric = False,        
        array=[np.max(example_1_simulation_array[-1:,]) - example_1_true_probability[-1], 
               np.max(example_2_simulation_array[-1:,]) - example_2_true_probability[-1], 
               np.max(example_3_simulation_array[-1:,]) - example_3_true_probability[-1]],
        arrayminus =[example_1_true_probability[-1] - np.min(example_1_simulation_array[-1:,]), 
                     example_2_true_probability[-1] - np.min(example_2_simulation_array[-1:,]), 
                     example_3_true_probability[-1] - np.min(example_3_simulation_array[-1:,])],
        visible=True
    )
)
trace2 = go.Scatter(
    x=['Green Scenario', 'Blue Scenario', 'Red Scenario'],    
    y=[example_1_true_probability[-1], example_2_true_probability[-1], example_3_true_probability[-1]],
    name='True Probability',
    mode = 'markers',
    marker = dict(color = 'red'),
)

data = [trace1, trace2]
#data = [trace2]

layout = go.Layout(
    barmode = 'group',
    showlegend = True,
    legend = dict(orientation = "h"),
    yaxis = dict(range=[0,1], title = "Probability of Winning"),
    title = "Tight Probability Approximation"
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig)


#### Below we are plotting the standard deviations through the simulations to see if they converged
#
#rolling_window = 10
#
#trace0 = go.Scatter(
#    y = rolling_std(example_1[:,0], rolling_window)[rolling_window-1:],
#    name = example_1_hand + '   ' + example_1_table
#)
#trace1 = go.Scatter(
#    y = rolling_std(example_2[:,0], rolling_window)[rolling_window-1:],
#    name = example_2_hand + '   ' + example_2_table
#)
#trace2 = go.Scatter(
#    y = rolling_std(example_3[:,0], rolling_window)[rolling_window-1:],
#    name = example_3_hand + '   ' + example_3_table
#)
#trace3 = go.Scatter(
#    y = rolling_std(example_4[:,0], rolling_window)[rolling_window-1:],
#    name = example_4_hand + '   ' + example_4_table
#)
#layout = {
#    'shapes': [
#        # Line Horizontal
#        {
#            'type': 'line',
#            'x0': 0,
#            'y0': 0.005,
#            'x1': example_1.shape[0],
#            'y1': 0.005,
#            'line': {
#                'color': 'rgb(205, 12, 24)',
#                'width': 2,
#                'dash': 'dash'
#            },
#        }
#    ],
#    'showlegend': True,
#    'legend': dict(orientation = "h")
#}
#
#fig = fig = {
#    'data': [trace0, trace1, trace2, trace3],
#    'layout': layout,
#}
#
#plotly.offline.plot(fig)



# =============================================================================
#import pandas as pd
#simulated_name_array = mock_array + ['SimulatedProbabilityWinning', 'SimulatedProbabilityTie']
#probability_dataframe = pd.DataFrame(np.hstack((probabilityInputList, probabilityList.reshape(-1, 2))), columns = simulated_name_array)
#probability_dataframe.columns = pd.Index(simulated_name_array)
#probability_dataframe.to_csv("ProbabilityTrainingData_Set2.csv", header = True)
# =============================================================================


class probabilityApproximator():
    def __init__(self, sess, n_features, lr, use_existing_model, graph = None):
        self.sess = sess
        self._n_features = n_features
#        self._neurons1 = 24
#        self._neurons2 = 12
        self._neurons1 = 48
        self._neurons2 = 24
        self._neurons3 = 12
        
        if use_existing_model == True:
            self.inputs = graph.get_tensor_by_name("ProbabilityNetwork/Inputs:0")
            self.simulated_probability = graph.get_tensor_by_name("ProbabilityNetwork/ActualProbability:0")
            
            self.approximate_probability = graph.get_tensor_by_name("ProbabilityNetwork/Probability:0")
        else:
            with tf.variable_scope('ProbabilityNetwork'):        
                self.inputs = tf.placeholder(shape = [None, self._n_features], dtype = tf.float32, name = "Inputs")
                self.simulated_probability = tf.placeholder(shape = [None, 2], dtype = tf.float32, name = "ActualProbability")
#                self.simulated_probability = tf.placeholder(shape = [None, 3], dtype = tf.float32, name = "ActualProbability")
                
                self.weights = tf.Variable(tf.random_normal([self._n_features, self._neurons1], stddev = tf.sqrt(2/(self._n_features + self._neurons1))))
                self.bias = tf.Variable(tf.zeros([1, self._neurons1]) + 0.01)
                self.layer = tf.nn.elu(tf.matmul(self.inputs, self.weights) + self.bias)
                
                self.weights2 = tf.Variable(tf.random_normal([self._neurons1, self._neurons2], stddev = tf.sqrt(2/(self._neurons1 + self._neurons2))))
                self.bias2 = tf.Variable(tf.zeros([1, self._neurons2]) + 0.01)
                self.layer2 = tf.nn.elu(tf.matmul(self.layer, self.weights2) + self.bias2)        
                
                self.weights3 = tf.Variable(tf.random_normal([self._neurons2, 2], stddev = tf.sqrt(2/(self._neurons2 + 2))))
                self.bias3 = tf.Variable(tf.zeros([1, 2]) + 0.01)
                self.approximate_probability = tf.nn.sigmoid(tf.matmul(self.layer2, self.weights3) + self.bias3, name = "Probability")
#                self.weights3 = tf.Variable(tf.random_normal([self._neurons2, 3], stddev = tf.sqrt(2/(self._neurons2 + 3))))
#                self.bias3 = tf.Variable(tf.zeros([1, 3]) + 0.01)                
#                self.approximate_probability = tf.nn.softmax(tf.matmul(self.layer2, self.weights3) + self.bias3, name = "Probability") 
                
#                self.weights = tf.Variable(tf.random_normal([self._n_features, self._neurons1], stddev = tf.sqrt(2/(self._n_features + self._neurons1))))
#                self.bias = tf.Variable(tf.zeros([1, self._neurons1]) + 0.01)
#                self.layer = tf.nn.elu(tf.matmul(self.inputs, self.weights) + self.bias)
#                
#                self.weights2 = tf.Variable(tf.random_normal([self._neurons1, self._neurons2], stddev = tf.sqrt(2/(self._neurons1 + self._neurons2))))
#                self.bias2 = tf.Variable(tf.zeros([1, self._neurons2]) + 0.01)
#                self.layer2 = tf.nn.elu(tf.matmul(self.layer, self.weights2) + self.bias2)        
#                
#                self.weights3 = tf.Variable(tf.random_normal([self._neurons2, self._neurons3], stddev = tf.sqrt(2/(self._neurons2 + self._neurons3))))
#                self.bias3 = tf.Variable(tf.zeros([1, self._neurons3]) + 0.01)
#                self.layer3 = tf.nn.elu(tf.matmul(self.layer2, self.weights3) + self.bias3) 
#                
#                self.weights4 = tf.Variable(tf.random_normal([self._neurons3, 2], stddev = tf.sqrt(2/(self._neurons3 + 2))))
#                self.bias4 = tf.Variable(tf.zeros([1, 2]) + 0.01)                
#                self.approximate_probability = tf.nn.sigmoid(tf.matmul(self.layer3, self.weights4) + self.bias4, name = "Probability")                 
        
        with tf.variable_scope("Loss"):
            self.loss = tf.reduce_mean(tf.square(self.simulated_probability - self.approximate_probability))
            
        with tf.variable_scope("TrainNetwork"):
            if use_existing_model == True:
                self.train_op = tf.get_collection("Trainer", scope = "TrainNetwork")[0]
            else:
                optimizer = tf.train.AdamOptimizer(lr)
                self.train_op = optimizer.minimize(self.loss)
                tf.add_to_collection(name = "Trainer", value = self.train_op)
        
    def trainModel(self, inputs, simulated_probability, epochs, batch_size, inputs_test, simulated_probability_test, verbose = True):
        
        batches_per_epoch = inputs.shape[0]//batch_size
        training_error_array = np.zeros(epochs)
        testing_error_array = np.zeros(epochs)
        
        for i in range(epochs):
            shuffled_indexes = np.random.choice(inputs.shape[0], size = inputs.shape[0], replace = False)
            batch_num = 0
            epoch_error = 0
            for j in range(batches_per_epoch):
                current_index = shuffled_indexes[batch_num:(batch_num + batch_size)]
                current_X = inputs[current_index,]
                current_Y = simulated_probability[current_index,]
                
                _, error = self.sess.run([self.train_op, self.loss], {self.inputs: current_X, self.simulated_probability: current_Y})
                
                epoch_error += error
                batch_num += batch_size
            epoch_error /= batches_per_epoch
            if i % 100 == 0 and verbose == True:
                print("The error for epoch {} is {}".format(i, epoch_error))
            training_error_array[i] = self.sess.run(self.loss, {self.inputs: inputs, self.simulated_probability: simulated_probability})
            testing_error_array[i] = self.sess.run(self.loss, {self.inputs: inputs_test, self.simulated_probability: simulated_probability_test})
            
        return training_error_array, testing_error_array

import pandas as pd
test_csv1 = pd.read_csv("ProbabilityTrainingData_Set1.csv", index_col = 0)
test_csv2 = pd.read_csv("ProbabilityTrainingData_Set2.csv", index_col = 0)
test_csv = pd.concat([test_csv1, test_csv2])
probabilityInputList = test_csv.values[:,:-2]; probabilityList = test_csv.values[:,-2:]

#
sess = tf.Session()
use_existing_model = False
graph = None
probabilityFunction = probabilityApproximator(sess, probabilityInputList.shape[1], 0.0005, use_existing_model, graph)
sess.run(tf.global_variables_initializer())


n_training_set = 225000
train_X, test_X = probabilityInputList[:n_training_set,], probabilityInputList[n_training_set:,]
train_Y, test_Y = probabilityList[:n_training_set,], probabilityList[n_training_set:,]

#new_train_Y = np.zeros((train_Y.shape[0], 3)); new_test_Y = np.zeros((test_Y.shape[0], 3))
#new_train_Y[:,:2] = train_Y; new_train_Y[:,2] = 1 - np.sum(train_Y, axis = 1); train_Y = new_train_Y
#new_test_Y[:,:2] = test_Y; new_test_Y[:,2] = 1 - np.sum(test_Y, axis = 1); test_Y = new_test_Y



training_error_array, testing_error_array = probabilityFunction.trainModel(train_X, train_Y, 10000, 250, test_X, test_Y)

# The split is always 90% Train and 10% Test. Batch size is always 1% of the total data sample

#training_error_1000 = training_error_array
#testing_error_1000 = testing_error_array
#
#plt.plot(training_error_1000)
#plt.plot(testing_error_1000)
#plt.plot(testing_error_1000 - training_error_1000)


#training_error_10000 = training_error_array
#testing_error_10000 = testing_error_array
#
#plt.plot(training_error_10000)
#plt.plot(testing_error_10000)
#plt.plot(testing_error_10000 - training_error_10000)


#training_error_100000 = training_error_array
#testing_error_100000 = testing_error_array
#
#plt.plot(training_error_100000)
#plt.plot(testing_error_100000)
#plt.plot(testing_error_100000 - training_error_100000) #Plotting the three differences is a useful graph


training_error_250000 = training_error_array
testing_error_250000 = testing_error_array

#plt.plot(training_error_250000)
#plt.plot(testing_error_250000)
#plt.plot(testing_error_250000 - training_error_250000) #Plotting the three differences is a useful graph
##
#errorDataFrame = pd.read_csv("ErrorDataFrame.csv", index_col = 0)
#errorArray = errorDataFrame.values
#starting_point = 50
#training_error_1000 = errorArray[starting_point:,0]
#testing_error_1000 = errorArray[starting_point:,1]
#training_error_10000 = errorArray[starting_point:,2]
#testing_error_10000 = errorArray[starting_point:,3]
#training_error_100000 = errorArray[starting_point:,4]
#testing_error_100000 = errorArray[starting_point:,5]

error_df = pd.read_csv("ErrorDataFrame.csv", index_col = 0)
error_values = error_df.values

#trace0 = go.Scatter(
#    y = testing_error_1000 - training_error_1000,
#    name = '1,000 Instances'
#)
trace1 = go.Scatter(
    y = error_values[:,3] - error_values[:,2],
    name = '10,000 Instances'
)
trace2 = go.Scatter(
    y = error_values[:,5] - error_values[:,4],
    name = '100,000 Instances'
)
trace3 = go.Scatter(
    y = error_values[:,7] - error_values[:,6],
    name = '250,000 Instances'
)
layout = {
    'showlegend': True,
#    'legend': dict(orientation = "h"),
    'yaxis': dict(range=[-0.0005,0.0008], title='Testing Error - Training Error'),
    'xaxis': dict(title='Epochs'),
    'title': 'Model Generalization',
}

fig = fig = {
#    'data': [trace0, trace1, trace2, trace3],
    'data': [trace1, trace2, trace3],
    'layout': layout,
}

plotly.offline.plot(fig)


#error_array = np.hstack((training_error_1000.reshape(-1, 1), testing_error_1000.reshape(-1, 1), 
#                         training_error_10000.reshape(-1, 1), testing_error_10000.reshape(-1, 1), 
#                         training_error_100000.reshape(-1, 1), testing_error_100000.reshape(-1, 1),
#                         training_error_250000.reshape(-1, 1), testing_error_250000.reshape(-1, 1)))
#column_names = ['TrainingError_1000_Instances', 'TestingError_1000_Instances', 
#                'TrainingError_10000_Instances', 'TestingError_10000_Instances', 
#                'TrainingError_100000_Instances', 'TestingError_100000_Instances',
#                'TrainingError_250000_Instances', 'TestingError_250000_Instances']
#error_df = pd.DataFrame(error_array, columns = column_names)
#error_df.to_csv('ErrorDataFrame.csv')

#"Read in the error CSV and make some graphics"
#
train_error = sess.run(probabilityFunction.loss, {probabilityFunction.inputs: train_X, probabilityFunction.simulated_probability: train_Y})
test_error = sess.run(probabilityFunction.loss, {probabilityFunction.inputs: test_X, probabilityFunction.simulated_probability: test_Y})

print("\nTrain Error: {:.4f} \nTest Error: {:.4f}".format(train_error, test_error))

predicted_train_probs = sess.run(probabilityFunction.approximate_probability, {probabilityFunction.inputs: train_X})
predicted_test_probs = sess.run(probabilityFunction.approximate_probability, {probabilityFunction.inputs: test_X})

train_prob_difference = abs(predicted_train_probs - train_Y); print(np.mean(train_prob_difference, axis = 0))
test_prob_difference = abs(predicted_test_probs - test_Y); print(np.mean(test_prob_difference, axis = 0))

errorTableColumns = ['Training Set', 'Testing Set']
errorTableRows = ['0.5%', '1.0%', '2.0%', '3.0%', '4.0%', '5.0%', '10.0%', '20.0%']
pokerErrorTable = np.zeros((len(errorTableRows), len(errorTableColumns)))
columns = 0

pokerErrorTable[0,0] = (sum(train_prob_difference < 0.005) / len(train_prob_difference))[columns]
pokerErrorTable[1,0] = (sum(train_prob_difference < 0.01) / len(train_prob_difference))[columns]
pokerErrorTable[2,0] = (sum(train_prob_difference < 0.02) / len(train_prob_difference))[columns]
pokerErrorTable[3,0] = (sum(train_prob_difference < 0.03) / len(train_prob_difference))[columns]
pokerErrorTable[4,0] = (sum(train_prob_difference < 0.04) / len(train_prob_difference))[columns]
pokerErrorTable[5,0] = (sum(train_prob_difference < 0.05) / len(train_prob_difference))[columns]
pokerErrorTable[6,0] = (sum(train_prob_difference < 0.1) / len(train_prob_difference))[columns]
pokerErrorTable[7,0] = (sum(train_prob_difference < 0.2) / len(train_prob_difference))[columns]

pokerErrorTable[0,1] = (sum(test_prob_difference < 0.005) / len(test_prob_difference))[columns]
pokerErrorTable[1,1] = (sum(test_prob_difference < 0.01) / len(test_prob_difference))[columns]
pokerErrorTable[2,1] = (sum(test_prob_difference < 0.02) / len(test_prob_difference))[columns]
pokerErrorTable[3,1] = (sum(test_prob_difference < 0.03) / len(test_prob_difference))[columns]
pokerErrorTable[4,1] = (sum(test_prob_difference < 0.04) / len(test_prob_difference))[columns]
pokerErrorTable[5,1] = (sum(test_prob_difference < 0.05) / len(test_prob_difference))[columns]
pokerErrorTable[6,1] = (sum(test_prob_difference < 0.1) / len(test_prob_difference))[columns]
pokerErrorTable[7,1] = (sum(test_prob_difference < 0.2) / len(test_prob_difference))[columns]

pokerErrorTable_winning_df = pd.DataFrame(pokerErrorTable, index = errorTableRows, columns = errorTableColumns)
pokerErrorTable_winning_df.index.name = 'Deviation from Actual'
pokerErrorTable_winning_df
#pokerErrorTable_tie_df = pd.DataFrame(pokerErrorTable, index = errorTableRows, columns = errorTableColumns)
#pokerErrorTable_tie_df.index.name = 'Deviation from Actual'
#pokerErrorTable_tie_df

#pokerErrorTable_winning_df.to_csv('ErrorTableWinning.csv')
#
#import matplotlib.pyplot as plt
#
#plt.plot(train_prob_difference)
#plt.plot(test_prob_difference)
#
#
## The AI is having a hard time detecting that it will win when it has the overcard that is the same suit as the flush on the table - we need more samples to make the prediction more robust
#print(np.max(train_prob_difference[:,0])); max_index = np.argmax(train_prob_difference[:,0]); print(max_index)
print(np.max(test_prob_difference[:,0])); max_index = np.argmax(test_prob_difference[:,0]); print(max_index)
#
#train_prob_difference[max_index]
#sampleHands[max_index]
#sampleTableCards[max_index]
#predicted_train_probs[max_index]
#train_Y[max_index]
#probabilityInputList[max_index,]
#findHandStatus(sampleTableCards[max_index], [])
#simulateProbability(sampleHands[max_index], sampleTableCards[max_index], simulationDeck, 1000)[-1]
#

test_prob_difference[max_index]
predicted_test_probs[max_index]
test_Y[max_index]
test_X[max_index,]

sess.run(probabilityFunction.approximate_probability, {probabilityFunction.inputs: test_X[test_X[:,18] == 1,]})
test_Y[test_X[:,18] == 1]
test_X[test_X[:,18] == 1,]

tester_hand = ['3_H', '10_H']
tester_deck = pokerDeck()
tester_table = ['5_S', '6_C', '7_S', '8_D', '9_S']
#tester_deck.evaluateHand([])
simulationDeck = pokerDeck()
simulateProbability(tester_hand, ['5_S', '6_C', '7_S', '8_D', '9_S'], simulationDeck, 1000)[-1]

evaluationDeck = pokerDeck()
tableEvaluationDeck = pokerDeck()
evaluationDeck.shuffleDeck(); evaluationDeck.table = tester_table
sampleCurrentHand, sampleTempBestCards = evaluationDeck.evaluateHand(tester_hand)
sampleCurrentRanking = simulationDeck.handRanking(sampleCurrentHand)
probArray = fetchProbabilityArray(tester_hand, tester_table, sampleCurrentRanking)

# I want to get my status irrespective of the table cards (because those are shared)
preflopStatusDict = findHandStatus(tester_hand, [])
statusArray = statusDictToInputArray(preflopStatusDict, "Hand", tester_hand, None)
if len(tester_table) != 0:
    tableStatusDict = findHandStatus(tester_table, [])
else:
    tableStatusDict = {}
tableStatusArray = statusDictToInputArray(tableStatusDict, "Table", tester_table, tableEvaluationDeck)

if len(tester_table) == 0:
    tableStatus = [1,0,0,0]
elif len(tester_table) == 3:
    tableStatus = [0,1,0,0]
elif len(tester_table) == 4:
    tableStatus = [0,0,1,0]
elif len(tester_table) == 5:
    tableStatus = [0,0,0,1]

tester_input = np.concatenate((probArray, statusArray, tableStatusArray, tableStatus))
sess.run(probabilityFunction.approximate_probability, {probabilityFunction.inputs: tester_input.reshape(1, -1)})

##### CREATE A HEURISTIC-BASED AI #####

class heuristicAgent():
    def __init__(self):
        self.bet_threshold = 0.55
        self.call_threshold = 0.65
        self.raise_threshold = 0.8
        
        self.fold_threshold = 0.5
        
        self.epsilon = 0.1
        
    def takeAction(self, probability, bigBlind, chipCount, previous_action, previous_bet):
        if previous_action == "Check" or previous_action is None:
            if np.random.rand(1)[0] < self.epsilon:
                decision = np.random.choice(['Check', 'Bet'])
                if decision == "Check":
                    amountBet = 0
                elif decision == "Bet":
                    amountBet = min(bigBlind + (np.random.rand()/5) * chipCount, chipCount)
            else:
                if probability >= self.bet_threshold:
                    decision = "Bet"
                    amountBet = min(bigBlind + (probability - self.bet_threshold) * chipCount, chipCount)
                else:
                    decision = "Check"
                    amountBet = 0
        elif previous_action == "Bet":
            if probability >= self.raise_threshold:
                decision = "Bet"
                amountBet = min(previous_bet + (probability - self.call_threshold) * chipCount, chipCount)
            elif probability >= self.call_threshold:
                decision = "Check"
                amountBet = 0
            else:
                decision = "Fold"
                amountBet = 0
        return decision, amountBet


#saver = tf.train.Saver()
#saver.save(sess, "Probability Model/ProbabilityApproximator")  

Prob_Big_Train_Error = (9 * 4 * 51 * 9 * 4) / nCr(52, 7)
Prob_Big_Test_Error = (nCr(52, 2) * 11 * nCr(4, 3) * 10 * nCr(4, 2)) / nCr(52, 7)

1/Prob_Big_Train_Error*4
1/Prob_Big_Test_Error*4


different_hole_cards = nCr(52, 2)
different_hole_flop = different_hole_cards * nCr(50, 3)
different_hole_flop_turn = different_hole_flop * nCr(47, 1)
different_hole_flop_turn_river = different_hole_flop_turn * nCr(46, 1)

different_plays_while_hole = nCr(50, 5) * nCr(45, 2)
different_plays_while_flop = nCr(47, 2) * nCr(45, 2)
different_plays_while_turn = nCr(46, 1) * nCr(45, 2)
different_plays_while_river = nCr(45, 2)
