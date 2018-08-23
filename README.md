# Poker Probability Approximation with Deep Learning

This project uses a neural network to quickly compute the probability of a hand ending in a win or tie. While lookup tables can be used, they are memory-intensive and cannot be stored in memory-constrained environments, such as mobile applications. Storing the weights in either numpy or tensorflow drastically reduces the memory required. 

The learned model can be used in any betting round of Texas Hold'Em Poker.

## Getting Started

To get started, clone this repo and open the file `pokerDeepLearningModel.py`

You will see three variables near the top of the file which you can toggle before running 

```
num_data_points = 1000           # The number of instances we want in our sample dataset
use_existing_model = True        # Do you want to use a pre-computed model or train a new one?
inference_sample_size = 100      # Size of sample to test the model on
```

The file outputs the Mean Absolute Error (MAE) for the sample in which you are testing on 

## Deployment

The learned model can easily be loaded and used as an input to a heuristic-based agent or a machine learning-based agent. 

```
probability_saver = tf.train.import_meta_graph("Probability Model/ProbabilityApproximator.meta")
probability_saver.restore(sess, tf.train.latest_checkpoint("Probability Model"))

graph = tf.get_default_graph()
probabilityFunction = probabilityApproximator(sess, probabilityInputList.shape[1], 0.0005, use_existing_model, graph)
```

A popular heuristic implementation is to use the probabilities obtained from the neural network with the Kelly Criterion (with some noise to reduce predictability). Conversely, with a machine learning agent, we can use a function approximation for the policy and feed these probabilities as some of the inputs.

## Work in Progress

The combinatorics for straight flush need to be updated in the `pokerCombinatorics.py` file
