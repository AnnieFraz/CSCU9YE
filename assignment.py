import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

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

def plot_colours(col, perm, title):
	assert len(col) == len(perm)
	
	ratio = 10 # ratio of line height/width, e.g. colour lines will have height 10 and width 1
	img = np.zeros((ratio, len(col), 3))
	for i in range(0, len(col)):
		img[:, i, :] = colours[perm[i]]

	fig, axes = plt.subplots(1, figsize=(8,4)) # figsize=(width,height) handles window dimensions
	axes.imshow(img, interpolation='nearest')
	axes.axis('off')
	plt.suptitle(title)    #added
	plt.show()


def greedy(col):
    original_colours = copy.deepcopy(col)
    sorted = []
    euclidean_distances = []
    greedy_sol = []
    # Getting a random start colour
    start_colour_index = random.randint(0, len(col)-1)
    start_colour = original_colours[start_colour_index]
    greedy_sol.append(start_colour_index)
    sorted.append(start_colour) #gets all the colours once sorted
    #Delete the colour from list of colours
    del original_colours[start_colour_index]
    next_colour = (0.0,0.0,0.0) #Initialising next colour
    while (len(original_colours) != 0): #To check whether colours is empty
        shortest_dis = 1000 #arbitrary starting value, just has to be greater than any possible distance
        for colour in original_colours:#Going through the list of colours
            distance = euclidean(start_colour, colour) #Calculating distance
            if (distance <= shortest_dis): #checking whether it is the shortest distance
                next_colour = colour #Reassigning next colour to be current value
                shortest_dis = distance # Reassigning shortestest to be current value
        euclidean_distances.append(shortest_dis)
        #Working out the index of the colour
        index = col.index(next_colour)
        greedy_sol.append(index)
        #Removing the colour so we know that that colour has been analysed.
        original_colours.remove(next_colour)
        start_colour = next_colour #Reassigning start colour to current value
    return greedy_sol, euclidean_distances





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
    print len(solution)
    print len(list_of_values)
    print solution
    print list_of_values
    return solution, list_of_values

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
        curr_solution, valList = hill_climbing(200)

        #Calculate total distance
        curr_dist = evaluate(curr_solution)

        #Determine if new solution is better, if it is copy it into the 'best' variables
        if(curr_dist < best_dist):
            best_dist = curr_dist
            best_solution = copy.deepcopy(curr_solution)
            best_sol_list = copy.deepcopy(valList)
        dist_list.append(curr_dist)
        
    return dist_list, best_solution, best_dist, best_sol_list

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
    result = math.sqrt( ((R2 - R1)**2) + ((G2 - G1)**2) + ((B2 - B1)**2) )

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

# Generate Random Neighbour
def generate_random_neighbour(solution):
    neighbour = []
    index1 = 0
    index2 = 0
    temp = []

    #Create copy of solution to make the nieghbour from
    neighbour = copy.deepcopy(solution)
    #print 'Before: ', neighbour
    
    #Calculate random indices
    index1 = random.randint(0, len(solution) - 1)
    index2 = random.randint(0, len(solution) - 1)

    #Flip range of indexes between two the random indexes
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

#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path) # Change the working directory so we can read the file

ncolors, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 500 # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

#Greedy Heuristic Algorithm
start = timeit.default_timer()
greedy_sol, distances = greedy(test_colours)
plot_colours( test_colours, greedy_sol, 'Greedy')
stop = timeit.default_timer()
print('Time: ', stop - start)

#permutation = random.sample(range(test_size), test_size) # produces random pemutation of lenght test_size, from the numbers 0 to test_size -1

'''
#Perform Hill Climb on the random permutation created above
final_sol, list_values = hill_climbing(200)
print 'Hill Climbing:'
#print 'Distances: \n', list_values
plot_colours(test_colours, final_sol, 'Hill Climb')

#Plot line graph to shows decreasing distances (for hill climb)
plt.figure()
plt.suptitle('Hill Climbing Algorithm Line Graph')
plt.plot(list_values) 
plt.ylabel("Distance Value")
plt.xlabel("X label")
plt.show()

#Perform multi-hill climb
d_list, multi_final_sol, sol_distance, hc_sol_list = multi_hc(30)
print '\nMulti Hill Climbing'
#print d_list
print'\nSolution Distance: ', sol_distance
plot_colours(test_colours, multi_final_sol, 'Multi-Hill Climb')

#Plot line graph to shows decreasing distances (for MULTI hill climb)
plt.figure()
plt.suptitle('Multi-Start Hill Climbing Algorithm Boxplot')
plt.boxplot(d_list)
plt.xlabel("Multi-Hill Climb")
plt.ylabel("Distance Value")
plt.show()
'''