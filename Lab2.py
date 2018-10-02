# The knapsack problem
# Gabriela Ochoa

import os
import matplotlib.pyplot as plt
from pylab import *
import random as rnd


# Single knapsack problem

# Read the instance  data given a file name. Returns: n = no. items,
# c = capacity, vs: list of itmen vamies, ws: list of item weigths



def read_kfile(fname):
    with open(fname, 'rU') as kfile:
        lines = kfile.readlines()     # reads the whole file
    n = int(lines[0])
    c = int(lines[n+1])
    vs = []
    ws = []
    lines = lines[1:n+1]   # Removes the first and last line
    for l in lines:
        numbers = l.split()   # Converts the string into a list
        vs.append(int(numbers[1]))  # Appends value, need to convert to int
        ws.append(int(numbers[2]))  # Appends weigth, need to convert to int
    #TASK1

    plt.figure()
    plt.plot(ws, vs,'yo')
    plt.title('Values and weights')
    plt.xlabel('Weights')
    plt.ylabel('Values')
    plt.show()
    return n, c, vs, ws

dir_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the file is located
os.chdir(dir_path)  # Change the working directory so we can read the file
knapfile = 'knap20.txt'
nitems, cap, values, weights = read_kfile(knapfile)


#TASK2
def constructive(items ,capacity, itemValue, itemWeight):
    knapsack = []
    weight = 0
    found = 0
    while (found == 0):
    #for item in items:
        if(min(itemWeight)>(capacity-weight)):
            found = 1
        else:
            best = max(itemValue)
            i = itemValue.index(best)
            if (itemWeight[i]<=(capacity-weight)):
                knapsack.append(i)
                weight = weight +itemWeight[i]
            del itemValue[i]
            del itemWeight[i]
    return knapsack, weight

#TASK3
def random_sol(n):
    random_array = []
    for i in range(n):
        number = rnd.randint(0, 1)
        random_array.append(number)
    return random_array

#TASK4
def evaulate(sol):
    total_value = 0
    total_wei = 0
    for i in range(len(sol)):
        if sol[i] == 1:
            total_value += values[i]
            total_wei += weights[i]
    return total_value, total_wei


#TASK5
def random_search(tries):
    best_val = 0
    best_weight = 0
    bestSol = []
    for i in range(tries):
        array = random_sol(tries)
        total_val, total_wei = evaulate(array)
        if (total_val > best_val and total_wei<=cap):
                best_val = total_val
                best_weight = total_wei
                bestSol = array
    return best_val, best_weight, bestSol

knapsack, weight = constructive(nitems, cap, values, weights)
print "knapsack: ", knapsack
print 'weight', weight


'''
print 'Random Sol method'
random_array = random_sol(nitems)
print 'Evaluate Method'
total_val, total_wei = evaulate(random_array)
print 'Totatl value', total_val
print 'Total Weight', total_wei

print 'Random Search Method'
best_val, best_weight, bestSol = random_search(11)
print 'Best value', best_val
print 'best weight', best_weight
print 'best solution array', bestSol



'''
