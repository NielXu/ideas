# AI
Some algorithms related to artificial intelligence. Most of them are from [CSCD84](https://utsc.calendar.utoronto.ca/course/cscd84h3), which is very interesting to study if you are interested in AI.


## bayes_net.py
__From Wikipedia:__
A Bayesian network (also known as a Bayes network, belief network, or decision network) is a probabilistic graphical model that represents a set of variables and their conditional dependencies via a directed acyclic graph (DAG).

This script is a very basic example of Bayesian Network including four variables: Cloudy(C), Sprinkler(S), Rain(R) and Wet grass(W).
- Sprinkler depends on cloudy (C -> S)
- Rain depends on cloudy (C -> R)
- Wet grass depends on sprinkler and rain (S, R -> W)

It contains two parts: random sampling to all variables and random sampling with observed variables.
