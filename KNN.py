import csv
import random
import math
import operator
import matplotlib.pyplot as iitg

csvfile=open('iris.data.csv', 'r')
lines = csv.reader(csvfile)
dataset = list(lines)
trainingSet=[]
testSet=[]
finalTestSet=[]
finalTrainingSet=[]

for x in range(0,len(dataset)):
	    for y in range(len(dataset[x])-1):
	        dataset[x][y] = float(dataset[x][y])

def finalloadDataset():
	length=int(math.ceil(float(len(dataset))*0.7))
	random.shuffle(dataset)
	for x in range(0,length):
		finalTrainingSet.append(dataset[x])
	for x in range(length,len(dataset)):
		finalTestSet.append(dataset[x])
def loadDataset():
	length=int(math.ceil(float(len(finalTrainingSet))*0.8))
	random.shuffle(finalTrainingSet)
	for x in range(0,length):
		trainingSet.append(finalTrainingSet[x])
	for x in range(length,len(finalTrainingSet)):
		testSet.append(finalTrainingSet[x])
def manhattanDistance(instance1, instance2, dimension):
	distance = 0
	for x in range(dimension):
		diff=instance1[x]-instance2[x]
		if (diff > 0):
			distance+=diff
		else:
			distance+= -diff		
	return distance
def finalgetNeighbours(testInstance,k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(finalTrainingSet)):
		dist = manhattanDistance(testInstance, finalTrainingSet[x], length)
		distances.append((finalTrainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	return distances[0:k]
def getNeighbours(testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = manhattanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	return distances[0:k]
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][0][-1]
		if response in classVotes:
			classVotes[response] += k-x# distance-weighted contribution 
		else:
			classVotes[response] = k-x
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
def finalgetAccuracy(predictions):
	correct=0.0
	for x in range(len(predictions)):
		if (predictions[x]==finalTestSet[x][-1]):
			correct += 1.0
	accuracy=(correct/float(len(predictions)))
	return accuracy
def getAccuracy(predictions):
	correct=0.0
	for x in range(len(predictions)):
		if (predictions[x]==testSet[x][-1]):
			correct += 1.0
	accuracy=(correct/float(len(predictions)))
	return accuracy

finalloadDataset()

noOfClasses=[]
for x in range(len(dataset)):
	if dataset[x][-1] not in noOfClasses:
		noOfClasses.append(dataset[x][-1])
c=len(noOfClasses)
print c
kp=[]
incr=2
for x in range(10):
	if (c%2==0):
		kp.append(c-1+incr)
	else:
		if ((c+incr)%c)!=0:
			kp.append(c+incr)
	incr+=2

counter=1
max=0
kmax=kp[0]
accr=[]
karr=[]
for i in range(5):
	k=kp[i]
	accuracy=0
	for y in range(5):#5-fold cross - validation
		loadDataset()
		predictions=[]
		for x in range(len(testSet)):
			neighbours=getNeighbours(testSet[x],k)
			result=getResponse(neighbours)
			predictions.append(result)
		accuracy += getAccuracy(predictions)
	print "for k="+repr(k)+"  accuracy= "+repr(accuracy*20)+"%"
	accr.append(accuracy*20)
	karr.append(k)
	if (accuracy>max):kmax=k
	

print "Best result when k= "+ repr(kmax)
fpredictions=[]
for x in range(len(finalTestSet)):
	neighbours=finalgetNeighbours(finalTestSet[x],kmax)
	result=getResponse(neighbours)
	fpredictions.append(result)
accuracy=finalgetAccuracy(fpredictions)
print "overall accuracy= "+ repr(accuracy*100)+ "%"

iitg.plot(karr,accr)
iitg.show()











