#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 21:33:07 2018

@author: brandinho
"""

from pathlib import Path
import random
import numpy as np
import tensorflow as tf
from pokerDeck import pokerDeck
from pokerProbabilities import fetchProbabilityArray, statusDictToInputArray, simulateProbability
from pokerCombinatorics import findHandStatus
from pokerNeuralNetwork import probabilityApproximator



sampleDeck = pokerDeck()         # We use the pokerDeck class to draw cards from
sampleHands = []                 # We make an empty list to append the hole cards to
tableCardsOptions = [0, 3, 4, 5] # We will randomly select from this list to determine how many cards appear on the table
sampleTableCards = []            # We make an empty list to append the board cards to
num_data_points = 1000           # The number of instances we want in our sample dataset

# Create sample data to train on
for i in range(num_data_points):
    sampleDeck.shuffleDeck()
    
    sampleHands.append(sampleDeck.currentDeck[:2])
    cleanDeck = sampleDeck.currentDeck[2:] # After we take the two hole cards we remove them from the deck
    
    sampleTableCards.append(cleanDeck[:random.choice(tableCardsOptions)])
    
    

# Below we create a mock array to get the dimensionality (These are all the inputs for our model)
mock_array = ['prob1', 'prob2', 'prob3', 'prob4', 'prob5', 'prob6', 'prob7', 'prob8', 
              'pairStatusHand', 'suitedStatusHand', 'straightGapStatusHand', 'lowCardHand', 'highCardHand',
              'pairStatusTable', 'suitedStatusTable', 'straightGapStatusTable', 'tripleStatusTable', 'TwoPairStatusTable', 
              'FullHouseStatusTable', 'RunnerRunnerStatusTable', 'SingleRunnerStatusTable', 
              'Straight - Table', 'Flush - Table', 'Four of a Kind - Table', 'Straight Flush - Table',
              'preflopOneHot', 'flopOneHot', 'turnOneHot', 'riverOneHot']

# We create multiple decks that serve different purposes when creating the input vectors
simulationDeck = pokerDeck()
evaluationDeck = pokerDeck()
tableEvaluationDeck = pokerDeck()

# We initialize empty arrays for the inputs and the labels
probabilityInputList = np.zeros((len(sampleHands), len(mock_array)))
probabilityList = np.zeros((len(sampleHands),2))

# We run through the loop to generate the inputs and labels to use during training
for j in range(len(sampleHands)):
    
    # We print which iteration we are on every 100 instances to keep track of our status
    if j % 100 == 0:
        print('You are at iteration {}'.format(j))

    """
    Below we calculate the probability of getting various hand rankings
    
    If we achieved a certain hand, all hands at least as good as it get a 1 assigned
    All other hands get a probability assigned
    """
    evaluationDeck.shuffleDeck(); evaluationDeck.table = sampleTableCards[j]
    sampleCurrentHand, _ = evaluationDeck.evaluateHand(sampleHands[j])
    sampleCurrentRanking = simulationDeck.handRanking(sampleCurrentHand)
    probArray = fetchProbabilityArray(sampleHands[j], sampleTableCards[j], sampleCurrentRanking)
    
    # Below we find the state of our hole cards using a combination of variables
    preflopStatusDict = findHandStatus(sampleHands[j], [])
    statusArray = statusDictToInputArray(preflopStatusDict, "Hand", sampleHands[j], None)
    
    # Below we find the state of the board cards using a combination of variables
    if len(sampleTableCards[j]) != 0:
        tableStatusDict = findHandStatus(sampleTableCards[j], [])
    else:
        tableStatusDict = {}
    tableStatusArray = statusDictToInputArray(tableStatusDict, "Table", sampleTableCards[j], tableEvaluationDeck)
    
    # Below we create a one-hot encoding of the betting round state
    if len(sampleTableCards[j]) == 0:
        tableStatus = [1,0,0,0]
    elif len(sampleTableCards[j]) == 3:
        tableStatus = [0,1,0,0]
    elif len(sampleTableCards[j]) == 4:
        tableStatus = [0,0,1,0]
    elif len(sampleTableCards[j]) == 5:
        tableStatus = [0,0,0,1]
        
    # Below we combine all of the different states into one input vector (which is assigned to the input array)
    probabilityInputList[j,] = np.concatenate((probArray, statusArray, tableStatusArray, tableStatus))
    
    # Below we simulate the probability to use as our label
    temp_prob_array = simulateProbability(sampleHands[j], sampleTableCards[j], simulationDeck, 1000)
    probabilityList[j,] = temp_prob_array[-1,]



"""
We initialize the tensorflow graph for our model

We have the option to load the pre-computed neural network or to train a new model from scratch
"""

tf.reset_default_graph()
sess = tf.Session()
use_existing_model = True

if use_existing_model:
    my_probability_file = Path("Probability Model/checkpoint")
    if my_probability_file.is_file() == True:
        probability_saver = tf.train.import_meta_graph("Probability Model/ProbabilityApproximator.meta")
        probability_saver.restore(sess, tf.train.latest_checkpoint("Probability Model"))
        
        graph = tf.get_default_graph()
        probabilityFunction = probabilityApproximator(sess, probabilityInputList.shape[1], 0.0005, use_existing_model, graph)
    else:
        raise ValueError("You do not have an existing model, please change this variable to 'False'")
else:
    graph = None
    probabilityFunction = probabilityApproximator(sess, probabilityInputList.shape[1], 0.0005, use_existing_model, graph)
    sess.run(tf.global_variables_initializer())


if use_existing_model == False:
    
    # We split the data into a training and testing set
    n_training_set = 900
    train_X, test_X = probabilityInputList[:n_training_set,], probabilityInputList[n_training_set:,]
    train_Y, test_Y = probabilityList[:n_training_set,], probabilityList[n_training_set:,]
    
    # Perform Training
    training_error_array, testing_error_array = probabilityFunction.trainModel(train_X, train_Y, 10000, 25, test_X, test_Y)


# Perform Inference
sample_size = 100
test_predictions = sess.run(probabilityFunction.approximate_probability, {probabilityFunction.inputs: test_X[:sample_size,]})
test_labels = test_Y[:sample_size,]
test_MAE = np.mean(abs(test_predictions - test_labels), axis = 0)

print("\nMAE for the sample \nP(Win): {:.2f}% \nP(Tie): {:.2f}%".format(test_MAE[0]*100, test_MAE[1]*100))
