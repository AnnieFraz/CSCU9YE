import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

from Main import evaluate, euclidean, generate_random_solution, generate_random_neighbour 


#Constructive Heuristic
def greedy(perm):
    original_colours = copy.deepcopy(perm)
    #original_colours = perm[0:test_size]
    new_colours = copy.deepcopy(colours)
    sorted = []
    greedy_sol = []

    #Choose a random start colour
    start_colour_index = random.choice(original_colours)
    greedy_sol.append(start_colour_index) #gets all the colours once sorted

    #Delete the colour index from list of colours
    original_colours.remove(start_colour_index)
    next_colour_index = 0 #Initialising next colour

    while len(greedy_sol)  < test_size: #To check whether colours is empty
        #arbitrary starting value, just has to be greater than any possible distance
        shortest_dis = 1000 

        #Going through the list of colours
        for i in range(len(original_colours)):
            #Calculate distance
            distance = euclidean(colours[start_colour_index], colours[original_colours[i]]) 

            #Check whether it is the shortest distance
            if distance < shortest_dis: 
                next_colour_index = original_colours[i] #Reassigning next colour to be current value
                shortest_dis = distance # Reassigning shortest to be current value

        #Work out the index of the colour
        greedy_sol.append(next_colour_index)

        #Remove the colour so we know that that colour has been analysed.
        start_colour_index = next_colour_index
        original_colours.remove(next_colour_index)

    return greedy_sol
