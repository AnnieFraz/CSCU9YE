import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

from Main import evaluate, euclidean, generate_random_solution, generate_random_neighbour

def tabu_search(perm):
    solution = copy.deepcopy(perm)
    best_candidate = copy.deepcopy(perm)
    tabu_list = []
    distances = []
    no_of_neighbours = 10 #arbitrary starting value
    max_tabu_size = 20 #arbitrary starting value
    j = 0

    #Adding starting value to the List
    tabu_list.append(solution)

    #Termination Criteria
    while (j < 1000): #arbitrary starting value, the higher the number the better the solution
        i = 0
        neighbours = []
        for i in range(no_of_neighbours): #Generates 10 different random solutions/neighbours which is used later to find the best
            generate_neighbour = generate_random_neighbour(best_candidate)
            neighbours.append(generate_neighbour)

        #Iterates through the neighbours to find the latest best solution
        for neighbour in neighbours:
            if (neighbour not in tabu_list and evaluate(neighbour) < evaluate(best_candidate)):
                best_candidate = neighbour

        #Evaluates the best solution in comparison to the current one
        if (evaluate(best_candidate) < evaluate(solution)):
            solution = best_candidate
            distances.append(evaluate(solution))
