import matplotlib.pyplot as plt
import numpy as np
import random
import os 
import math
import copy
import timeit

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

        #List of all the best candidates
        tabu_list.append(best_candidate)

        #Deletes elements if the list gets too large
        if (len(tabu_list) > max_tabu_size):
            del tabu_list[0]
        j = j + 1

    return solution, distances

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

