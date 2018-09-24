
#TASK 1
import random as rnd

def ages_calculater(size):
	ages = []
	total = 0
	for i in range(size):
		number = rnd.randint(1,120)
		ages.append(number)
		print 'person: ',i,'age: ',number
		total = total + ages[i]
	average = total/size
	print 'My average is: ', average
	average_py = sum(ages)/size
	print 'Pythons Average is: ', average_py
	return ages, average

val1, val2 = ages_calculater(5)



#TASK 2
import random as rnd
import matplotlib.pyplot as plt


def ages_calculater2(size):
	ages = []
	total = 0
	for i in range(size):
		print i
		number = rnd.randint(1,120)
		ages.append(number)
		print 'person: ',i,'age: ',number
		total = total + ages[i]
	average = total/size
	print 'My average is: ', average
	average_py = sum(ages)/size
	print 'Pythons Average is: ', average_py

	plt.figure()
	plt.plot(ages) #This is the blue line
	plt.boxplot(ages)
	plt.show()

	return ages, average

val1, val2 = ages_calculater2(5)