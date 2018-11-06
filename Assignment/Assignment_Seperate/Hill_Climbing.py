import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

from Main import evaluate, euclidean, generate_random_solution, generate_random_neighbour

# Hill Climbing Algorithm
def hill_climbing(iteration):
    solution = []
    neigh_solution = []
    list_of_values = []
    sol_distance = 0
    neigh_distance = 0
    
    #Initial random solution
    solution = generate_random_solution()
    #plot_colours(test_colours, solution, 'Initial Hill Climb')
    
    #Loop for specified number of iterations
    for i in range(iteration):

        #Evaluate total distance of solution
        sol_distance = evaluate(solution)
        
        #Generate random neighbour to current solution
        neigh_solution = generate_random_neighbour(solution)

        #Evaluate total distance of neighbour solution
        neigh_distance = evaluate(neigh_solution)
        
        #Update solution if neighbour is better
        if(neigh_distance < sol_distance):
            solution = copy.deepcopy(neigh_solution)
            list_of_values.append(neigh_distance)

    #Return a list of the distance values at each iteration, and the best solution found
    return solution, list_of_values

#Multi Hill_climbing
def multi_hc(tries):
    curr_solution = []
    valList = []
    curr_dist = 0
    best_dist = 1000 #arbitrary starting value, just has to be greater than any possible distance
    best_solution = []
    best_sol_list = []
    dist_list = []
    
    for i in range(tries):
        #Hill Climb
        curr_solution, valList = hill_climbing(500)

        #Calculate total distance of current solution
        curr_dist = evaluate(curr_solution)

        #Determine if new solution is better, if it is copy it into the 'best' variables
        if(curr_dist < best_dist):
            best_dist = curr_dist
            best_solution = copy.deepcopy(curr_solution)
            best_sol_list = copy.deepcopy(valList)
        dist_list.append(curr_dist)
        
    return dist_list, best_solution, best_dist, best_sol_list
