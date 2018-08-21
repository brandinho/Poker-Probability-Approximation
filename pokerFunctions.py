#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 00:11:18 2018

@author: brandinho
"""

### Also try changing one line of code and attach the bet to the discrete network as a separate output (this could help regularize the network)

import numpy as np
import pokerProbabilities

def takeAction(tableProgression, players, position, probabilities, previous_action, current_bets, bigBlind, deck, hands, allIn, money, deepNuts, deepDummy, AImemoryP1, AImemoryP2, randomActions, abstractMemory, training_abstraction_dict, abstraction_dict, complete_memory_dict): 
    callNeeded = np.max(current_bets) - current_bets[position]
    
    if allIn == True:
        secondLastInput = 1
        lastInput = 1
    else:
        secondLastInput = callNeeded/money.chipCount[position]
        lastInput = money.currentPot/money.chipCount[position]
        
    if tableProgression == "PreFlop":
        progressionList = [1, 0, 0, 0]
    elif tableProgression == "Flop":
        progressionList = [0, 1, 0, 0]
    elif tableProgression == "Turn":
        progressionList = [0, 0, 1, 0]
    elif tableProgression == "River":
        progressionList = [0, 0, 0, 1]
        
    if previous_action == None:
        opponentActionList = [1, 0, 0]
    elif previous_action == 'Check':
        opponentActionList = [0, 1, 0]
    elif previous_action == 'Bet':
        opponentActionList = [0, 0, 1]
    
    input_array = np.array([probabilities[0], probabilities[1],
                            progressionList[0], progressionList[1], progressionList[2], progressionList[3],
                            secondLastInput, lastInput,
                            opponentActionList[0], opponentActionList[1], opponentActionList[2]]).reshape(1, -1)
    
    if players[position] == 'Player 0':
        memory = AImemoryP1.experience
    elif players[position] == 'Player 1':
        memory = AImemoryP2.experience
        
    if len(memory) == 2:
        training_abstract_input = memory[-2:,2:-5].reshape(1, -1, input_array.shape[1] - 2)
        abstractMemory.trainModel(training_abstract_input)
        training_abstraction = abstractMemory.getEmbedding(training_abstract_input)
        training_abstraction_dict[players[position]] = training_abstraction
    elif len(memory) > 2:
        training_abstract_input = np.vstack((training_abstraction_dict[players[position]], memory[-1:,2:-5])).reshape(1, -1, input_array.shape[1] - 2)
        abstractMemory.trainModel(training_abstract_input)
        training_abstraction = abstractMemory.getEmbedding(training_abstract_input)
        training_abstraction_dict[players[position]] = training_abstraction
        
    if len(memory) > 7:
        if players[position] in abstraction_dict:
            abstract_input = np.vstack((abstraction_dict[players[position]], memory[-7,2:-5])).reshape(1, -1, input_array.shape[1] - 2)
        else:
            abstract_input = memory[-8:-6,2:-5].reshape(1, -1, input_array.shape[1] - 2)
            
        abstraction = abstractMemory.getEmbedding(abstract_input)
        abstraction_dict[players[position]] = abstraction
        
        full_abstraction_array = np.zeros(input_array.shape[1]); full_abstraction_array[2:] = abstraction
        
        memory_enabled_input_array = np.hstack((full_abstraction_array.reshape(1, -1, input_array.shape[1]),
                                                memory[-6:,:-5].reshape(1, -1, input_array.shape[1]), 
                                                input_array.reshape(1, -1, input_array.shape[1])))
    elif len(memory) > 0:
        memory_enabled_input_array = np.hstack((memory[:,:-5].reshape(1, -1, input_array.shape[1]), 
                                                input_array.reshape(1, -1, input_array.shape[1]), 
                                                np.zeros((1, 7 - memory.shape[0], input_array.shape[1]))))
    else:
        memory_enabled_input_array = np.hstack((input_array.reshape(1, -1, input_array.shape[1]), 
                                                np.zeros((1, 7, input_array.shape[1]))))
    
    currentTimestep = min(len(memory) + 1, 8)
    
    if players[position] not in complete_memory_dict:
        complete_memory_dict[players[position]] = memory_enabled_input_array
    else:
        complete_memory_dict[players[position]] = np.vstack((complete_memory_dict[players[position]], memory_enabled_input_array))

#    sess.run(deepNuts.raw_decision, {deepNuts.state_values: memory_enabled_input_array, deepNuts.current_timestep: currentTimestep})
#    sess.run(deepNuts.bet_sigmoid_output, {deepNuts.state_values: memory_enabled_input_array, deepNuts.current_timestep: currentTimestep})

    if players[position] == 'Player 0':
        current_action, amountBet = deepNuts.makeDecision(memory_enabled_input_array, money.chipCount[position], callNeeded, bigBlind, randomActions, currentTimestep)
    elif players[position] == 'Player 1':
        current_action, amountBet = deepDummy.makeDecision(memory_enabled_input_array, money.chipCount[position], callNeeded, bigBlind, currentTimestep)
    amountBet -= callNeeded; amountBet = max(amountBet, 0)
    
    return current_action, amountBet, input_array, callNeeded, training_abstraction_dict, abstraction_dict, complete_memory_dict, currentTimestep


def fold(tableProgression, position, input_array, complete_memory_dict, timestep_dict, AImemoryP1, callNeeded, money, deepNuts, amountBet, policy_rewardP1, randomActions, players, i, m):
    
    print("\n" + tableProgression + "\n{} Folded, and {} won {} chips".format(players[position], players[(i+1)%2], money.currentPot))
        
    if players[position] == 'Player 0':
        AImemoryP1.insertExperience(np.hstack((input_array, [[0]], [[money.blinds[1]]], [[callNeeded]], 
                                               [[money.chipCount[position]]], [[amountBet]])))        
        rewardP1 = -money.currentPot/2
    elif players[position] == 'Player 1':
        rewardP1 = money.currentPot/2    
        
    money.chipCount[int(players[(i+1)%2][-1])] += money.currentPot
    
    rewardP1 /= (abs(rewardP1) + money.chipCount[0])
        
    if m == 0:
        policy_rewardP1, random_rewardP1 = rewardP1, rewardP1
    else:
        random_rewardP1 = rewardP1
    
#    sess.run(deepNuts.raw_decision, {deepNuts.state_values: memory_enabled_input_array, deepNuts.current_timestep: currentTimestep})
    
    if 'Player 0' in complete_memory_dict:     
        replayP1 = AImemoryP1.experience
        deepNuts.trainModel(complete_memory_dict['Player 0'], replayP1[:,-5], replayP1[:,-4], replayP1[:,-3], replayP1[:,-2], 
                            policy_rewardP1, randomActions, random_rewardP1, replayP1[:,-1], timestep_dict['Player 0'])
        
    #Roll the players and move onto the next hand
    players = np.roll(players, -1)
    money.chipCount = np.roll(money.chipCount, -1)
    
    return policy_rewardP1, random_rewardP1, players

def goAllIn(tableProgression, position, input_array, complete_memory_dict, timestep_dict, AImemoryP1, callNeeded, money, deepNuts, amountBet, policy_rewardP1, randomActions, players, m, deck, hands):
    print("\n" + tableProgression + "\n{} Called All-In with {} chips".format(players[position], callNeeded))

    if players[position] == 'Player 0':
        AImemoryP1.insertExperience(np.hstack((input_array, [[1]], [[money.blinds[1]]], [[callNeeded]], 
                                               [[money.chipCount[position]]], [[amountBet]])))
    
    if tableProgression == "PreFlop":
        deck.flipFlop()
    if tableProgression == "PreFlop" or tableProgression == "Flop":
        deck.flipTurn()
    if tableProgression == "PreFlop" or tableProgression == "Flop" or tableProgression == "Turn":
        deck.flipRiver()
    print(deck.table)
    money.chipCount[position] -= callNeeded
    money.addToPot(callNeeded)
    
    _, winner = deck.whoWins(hands)
    print("\n{} won {} chips".format(players[winner], money.currentPot))

    if winner != None and players[winner] == 'Player 0':
        rewardP1 = money.currentPot/2
    elif winner != None and players[winner] == 'Player 1':
        rewardP1 = -money.currentPot/2        
    if winner == None:
        rewardP1 = 0
        money.chipCount += int(money.currentPot/2)
    else:
        money.chipCount[winner] += money.currentPot            
        
    rewardP1 /= (abs(rewardP1) + money.chipCount[0])
        
    if m == 0:
        policy_rewardP1, random_rewardP1 = rewardP1, rewardP1
    else:
        random_rewardP1 = rewardP1

#    sess.run(deepNuts.raw_decision, {deepNuts.state_values: memory_enabled_input_array, deepNuts.current_timestep: currentTimestep})
    
    if 'Player 0' in complete_memory_dict:
        replayP1 = AImemoryP1.experience
        deepNuts.trainModel(complete_memory_dict['Player 0'], replayP1[:,-5], replayP1[:,-4], replayP1[:,-3], replayP1[:,-2], 
                            policy_rewardP1, randomActions, random_rewardP1, replayP1[:,-1], timestep_dict['Player 0'])
        
    #Roll the players and move onto the next hand
    players = np.roll(players, -1)
    money.chipCount = np.roll(money.chipCount, -1)
    
    return policy_rewardP1, random_rewardP1, players

