import os
import matplotlib.pyplot as plt
from pylab import *
import random as rnd
import copy


# Single knapsack problem

# Read the instance  data given a file name. Returns: n = no. items,
# c = capacity, vs: list of itmen vamies, ws: list of item weigths

def read_kfile(fname):
    with open(fname, 'rU') as kfile:
        lines = kfile.readlines()  # reads the whole file
    n = int(lines[0])
    c = int(lines[n + 1])
    vs = []
    ws = []
    lines = lines[1:n + 1]  # Removes the first and last line
    for l in lines:
        numbers = l.split()  # Converts the string into a list
        vs.append(int(numbers[1]))  # Appends value, need to convert to int
        ws.append(int(numbers[2]))  # Appends weigth, need to convert to int
    # TASK1
    '''
    plt.figure()
    plt.plot(ws, vs,'yo')
    plt.title('Values and weights')
    plt.xlabel('Weights')
    plt.ylabel('Values')
    plt.show()
    '''
    return n, c, vs, ws

dir_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the file is located
os.chdir(dir_path)  # Change the working directory so we can read the file
knapfile = 'knap20.txt'
nitems, cap, values, weights = read_kfile(knapfile)



# TASK2
def constructive(items, capacity, itemValue, itemWeight):
    knapsack = []
    weight = 0
    found = 0
    while (found == 0):
        # for item in items:
        if (min(itemWeight) > (capacity - weight)):
            found = 1
        else:
            best = max(itemValue)
            i = itemValue.index(best)
            if (itemWeight[i] <= (capacity - weight)):
                knapsack.append(i)
                weight = weight + itemWeight[i]
            del itemValue[i]
            del itemWeight[i]
    return knapsack, weight


# TASK3
def random_sol(n):
    random_array = []
    for i in range(n):
        number = rnd.randint(0, 1)
        random_array.append(number)
    return random_array


# TASK4
def evaluate(sol):
    total_value = 0
    total_wei = 0
    for i in range(len(sol)):
        if sol[i] == 1:
            total_value += values[i]
            total_wei += weights[i]
    return total_value, total_wei


# TASK5
def random_search(tries):
    best_val = 0
    best_weight = 0
    bestSol = []
    for i in range(tries):
        array = random_sol(tries)
        total_val, total_wei = evaluate(array)
        if (total_val > best_val and total_wei <= cap):
            best_val = total_val
            best_weight = total_wei
            bestSol = array
    return best_val, best_weight, bestSol

#*****LAB 3******
# LAB3
def random_sol_valid(n):
    binvalid = True
    while binvalid:
        s = random_sol(n)
        v, w = evaluate(s)
        binvalid = (w > cap)
    #print 'RANDOM SOL Value: ', v, 'WEIGHT:', w
    return s, v, w


# LAB3 Task 1
def random_search_valid(tries):
    bin_valid = True
    best_val = 0
    best_wei = 0
    best_sol = []
    # while bin_valid:
    for i in range(tries):
        array, total_val, total_wei = random_sol_valid(tries)
        # total_val, total_wei = evaulate(array)
        if total_val > best_val and total_wei <= cap:
            best_val = total_val
            best_wei = total_wei
            best_sol = array
    #print 'RANDOM SEARCH, Values - ', values, 'best value', best_val, 'best weight', best_wei
    return values, best_sol, best_val, best_wei


def local_optima(sol):
    best_sol = False
    best_weight = 0
    best_value = 0
    n_best_weight = 0
    n_best_value = 0
    n_sol = []
    best_value, best_weight = evaluate(sol)
    n_sol = sol[:]
    #while best_sol != True:
    for i in range(len(sol)):
        if (sol[i] == 0):
            n_sol[i] = 1
        else:
            n_sol[i] = 0
    n_best_value, n_best_weight = evaluate(n_sol)
    if (n_best_value > best_value and n_best_weight <= cap):
        best_sol = True
    else:
        best_sol = False
       # n_sol = []
    #print 'LOCAL OPTIMA: Value -', n_best_value, ' Weight-', n_best_weight
    #print 'LOCAL OPTIMA Better solution? ', best_sol
    return best_sol


def random_valid_neig(sol):
    random_point = rnd.randint(0, len(sol) - 1)
    n_sol = []
    n_best_weight = 0
    n_best_value = 0
    best_value = 0
    best_weight = 0
    best_sol = False
    binvalid = False
    
    best_value, best_weight = evaluate(sol)
    while binvalid == False:
        n_sol = sol[:]
        if (sol[random_point] == 0):
            n_sol[random_point] = 1
        elif (sol[random_point] == 1):
            n_sol[random_point] = 0
        n_best_value, n_best_weight = evaluate(n_sol)
        if (n_best_weight <= cap):
            best_sol = True
            binvalid = True
        #print 'RANDOM VALID NEIGHBOUR Better solution? ', best_sol
        return n_sol,  n_best_value, n_best_weight
       
        
'''
    print 'RANDOM VALID NEIGHBOUR best_value', n_best_value
    print 'RANDOM VALID NEIGHBOUR sol', n_sol
    print 'RANDOM VALID NEIGHBOUR best_weight', n_best_weight
    '''


def hill_climbing():
    optima_local = False

    solution = []
    solution_value = 0
    solution_weight = 0

    solution_neighbour = []
    neighbout_weight = 0
    neighbour_value = 0

    list_of_value = []


    while (optima_local == False):
        solution, values, weights = random_sol_valid(20)
        solution_value, solution_weight = evaluate(solution)
        solution_neighbour, neighbour_value, neighbour_weight = random_valid_neig(solution)
        if (neighbour_value > solution_value):
            list_of_value.append(neighbour_value)
            solution = copy.deepcopy(solution_neighbour)
            optima_local = local_optima(solution)
        #print list_of_value
        #print solution
    return solution, list_of_value



def multi_hc(tries):
    best_sol = []
    values = []
    big_list_values = []
    best_val = 0
    best_wei = 0

    for i in range(tries):
        hill_climb_sol,values = hill_climbing()
        big_list_values.append(values)
    if (max(values)>max(big_list_values)):
        best_sol = hill_climb_sol
        best_val, best_wei = evaluate(hill_climb_sol)

    return values, best_sol, best_val, best_wei


# *******PRACTICAL 3 *****
# THE Box plot wants the values
# RANDOM SOL VALID METHOD
print 'RANDOM SOL VALID METHOD'
sol, value, weight = random_sol_valid(nitems)
# RANDOM SEARCH VALID METHOD
print  'RANDOM SEARCH VALID METHOD'
rsv_values, rsv_sol, rsv_value, rsv_weight = random_search_valid(nitems)
# LOCAL OPTIMA
#sol2 = random_sol_valid(5)
print 'LOCAL OPTIMA METHOD'
local_optima_sol = local_optima(sol)
# RANDOM VALID NEIGHBOUR
print 'RANDOM VALID NEIGHBOUR'
rvn_sol, rvn_best_value, rvn_best_weight = random_valid_neig(sol)
# Hill Climbing
print 'HILL CLIMBING'
hill_sol, hill_values = hill_climbing()
#Multi Hill climbing
print 'MULTI HILL CLIMBING'
mhc_values, mhc_sol, mhc_val, mhc_wei = multi_hc(nitems)

plt.figure()
plt.plot(sort(hill_values))
plt.show()


results = [rsv_values, mhc_values]
plt.figure()
plt.boxplot(results,labels = ['random', 'hill-climbing'])
plt.show()




