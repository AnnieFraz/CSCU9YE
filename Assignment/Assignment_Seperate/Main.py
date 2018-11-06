import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

from Greedy import greedy
from Tabu import tabu_search
from Hill_Climbing import hill_climbing, multi_hc

#Authors: James Coburn and Anna Rasburn
#Python 2.7

# Reads the file  of colours
# Returns the number of colours in the file and a list with the colours (RGB) values
def read_file(fname):
    with open(fname, 'r') as afile:
        lines = afile.readlines()
    n = int(lines[3])    # number of colours  in the file
    col = []
    lines = lines[4:]    # colors as rgb values
    for l in lines:
        rgb = l.split()
        col.append(rgb)
    return n, col

# Display the colours in the order of the permutation in a pyplot window 
# Input, list of colours, and ordering  of colours.
# They need to be of the same length
#***ADDED*** Third parameter 'title' takes in a string to use as the title of the plot
def plot_colours(col, perm, title):
	assert len(col) == len(perm)
	
	ratio = 10 # ratio of line height/width, e.g. colour lines will have height 10 and width 1
	img = np.zeros((ratio, len(col), 3))
	for i in range(0, len(col)):
		img[:, i, :] = colours[perm[i]]

	fig, axes = plt.subplots(1, figsize=(8,4)) # figsize=(width,height) handles window dimensions
	axes.imshow(img, interpolation='nearest')
	axes.axis('off')
	plt.suptitle(title)#added
	plt.show()

# Evaluate solution (calculate sum of distances)
def evaluate(solution):
    total_distance = 0
    
    #Loop through each colour and total the distances between each
    for i in range(len(solution) - 1):
        total_distance = total_distance + euclidean(colours[solution[i]], colours[solution[i + 1]])
        
    return total_distance

# Calculate Euclidean Distance
def euclidean(colour1, colour2):
    #Data is stored as string so have to convert it to a float
    R1 = float(colour1[0])
    G1 = float(colour1[1])
    B1 = float(colour1[2])

    R2 = float(colour2[0])
    G2 = float(colour2[1])
    B2 = float(colour2[2])

    #Calculate Distance
    result = math.sqrt(((R2 - R1)**2) + ((G2 - G1)**2) + ((B2 - B1)**2))

    #Print check of variables
    #print ('c1: ', colour1)
    #print('c2: ', colour2)
    #print (result)
    
    return result

#Generate random solution
def generate_random_solution():
    solution = []

    #Generate random permutation
    solution = random.sample(range(test_size), test_size)
    
    return solution

#Generate Random Neighbour
def generate_random_neighbour(solution):
    neighbour = []
    index1 = 0
    index2 = 0
    temp = []

    #Create copy of solution to make the neighbour from
    neighbour = copy.deepcopy(solution)
    #print 'Before: ', neighbour
    
    #Calculate random indices
    index1 = random.randint(0, len(solution) - 1)
    index2 = random.randint(0, len(solution) - 1)

    #Flip range of indexes between two the random indexes
    #Determine which index is bigger to choose which variation of the swap to perform
    if(index1 > index2):
        while(index1 > index2):
            temp = neighbour[index1]
            neighbour[index1] = neighbour[index2]
            neighbour[index2] = temp
            index1 = index1 - 1
            index2 = index2 + 1
    else:
        while(index2 > index1):
            temp = neighbour[index1]
            neighbour[index1] = neighbour[index2]
            neighbour[index2] = temp
            index1 = index1 + 1
            index2 = index2 - 1
        
    #print 'After: ', neighbour
    return neighbour

#Prints the mean, median, and standard deviation given a list of distances
def stats(distances):
    distances = sorted(distances)
    print 'Mean = ', np.mean(distances)
    print 'Median = ', np.median(distances)
    print 'Standard Deviation = ', np.std(distances)


#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path) # Change the working directory so we can read the file

ncolors, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 500 # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

permutation = random.sample(range(test_size), test_size) # produces random pemutation of lenght test_size, from the numbers 0 to test_size -1

random_test_colours = random.sample(range(len(colours)), test_size)

#Task 1: Greedy Heuristic Algorithm
start = timeit.default_timer()
greedy_sol = greedy(permutation)
stop = timeit.default_timer()
greedy_distance = evaluate(greedy_sol)
plot_colours(test_colours, greedy_sol, 'Constructive Heuristic')
print 'Greedy Algorithm: '
print 'Time = ', stop - start, "sec"
print 'Solution Distance = ', greedy_distance


#Task 2: Perform Hill Climb on the random permutation created above
start = timeit.default_timer()
hc_sol, list_values = hill_climbing(4000)
stop = timeit.default_timer()
print '\nHill Climbing:'
print 'Run Time = ', stop - start, "sec"
print 'Solution Distance = ', evaluate(hc_sol)
#print 'Distances: \n', list_values
plot_colours(test_colours, hc_sol, 'Hill Climb')

#Task 2.1: Plot line graph to shows decreasing distances (for hill climb)
plt.figure()
plt.suptitle('Hill Climbing Algorithm Line Graph')
plt.plot(list_values) 
plt.ylabel("Distance Value")
plt.show()

#Task 3: Perform multi-hill climb
start = timeit.default_timer()
d_list, multi_final_sol, sol_distance, hc_sol_list = multi_hc(30)
stop = timeit.default_timer()
print '\nMulti Hill Climbing:'
stats(d_list)    #calculate and print mean, median, and standard deviation
print 'Run Time = ', stop - start, "sec"
print'Solution Distance = ', sol_distance
plot_colours(test_colours, multi_final_sol, 'Multi-Hill Climb')

#Task 3.1 Plot boxplot graph to show spread of hill climbing results found
plt.figure()
plt.suptitle('Multi-Start Hill Climbing Algorithm Boxplot')
plt.boxplot(d_list, labels=["Multi-Hill Climb"])
plt.ylabel("Distance Value")
plt.show()

#Task 4: Tabu Search
start_tabu = timeit.default_timer()
tabu_sol, tabu_distances = tabu_search(permutation)
stop_tabu = timeit.default_timer()
plot_colours(test_colours, tabu_sol, 'Tabu Search')
tabu_evaluate = evaluate(tabu_sol)  #calculate final distance
print '\nTabu Search:'
stats(tabu_distances)    #calculate and print mean, median, and standard deviation
print 'Time = ', stop_tabu - start_tabu, "sec"
print 'Solution Distance = ', tabu_evaluate

#Task 4.1 Plot Tabu Search line graph
plt.figure()
plt.suptitle('Tabu Search Algorithm Line Graph')
plt.plot(tabu_distances)
plt.ylabel("Distance Value")
plt.show()

#Task 5: Comparing Algorithms Boxplot
plt.figure(figsize=(7,6))
plt.suptitle('Distances by Different Algorithms')
plt.boxplot([list_values, d_list, tabu_distances], labels=['Hill-Climbing','Multi-Hill Climb','Tabu'] )
plt.xlabel("\nAlgorithms")
plt.ylabel("Distance Value")
plt.show()

