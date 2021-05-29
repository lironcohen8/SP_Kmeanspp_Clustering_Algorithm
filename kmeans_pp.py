# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
#import mykmeanssp

def isPositiveInt(s):
    try:
        i = int(s)
        return i>0 
    except:
        return False
    
    

def distance(vector1, vector2, dimension):
    '''Claculates the distance between two vectors'''
    dis = 0
    for i in range(1,dimension+1): #Runs for each dimension 
        dis += (vector1.iloc[0,i]-vector2.iloc[0,i])**2 
    return dis


def clacDi(vector, centroids, z, dimension):
    '''Calculates Di - the minimum distance of the vector from a centroid'''
    minDis = distance(vector, centroids[0], dimension) #Initiate the minimum distance to be the distance from the first centroid
    for i in range(z): #For each centroid (there are z at this point)
        dis = distance(vector, centroids[i], dimension)
        if dis < minDis:
            minDis = dis    
    return minDis


def initCentroids(vectors, k, numOfVectors, dimension):
    assert k<numOfVectors, "The number of clusters must be smaller than the number of vectors"
    np.random.seed(0)
    
    distances = [0 for i in range(numOfVectors)]
    initialcentroids = []
    initialCentroidsIndices = []
    
    #Get the first centroid
    i = np.random.randint(0, numOfVectors+1)
    initialcentroids.append(vectors.iloc[[i]])
    
    
    z=1
    while z<k:
        for i in range(numOfVectors): #Calc Di for each vector
            di = clacDi(vectors.iloc[[i]], initialcentroids, z, dimension)
            distances[i] = di
        z+=1
        
        #Calculate the probability to choose each vector as the next centroid
        sumDi = np.sum(distances)
        probabilities = [distances[i]/sumDi for i in range(numOfVectors)]
        
        #Chooses the next centroid based on the probabilities we calculated
        vecInd = np.random.choice(numOfVectors,p=probabilities)
        initialcentroids.append(vectors.iloc[[vecInd]])
    
    #Convert the initialcentroids from dataframes to simple lists
    #Create the initialCentroidsIndices list
    for i in range(len(initialcentroids)):
        initialcentroids[i] = initialcentroids[i].values.tolist()[0]
        initialCentroidsIndices.append(int(initialcentroids[i][0]))
        initialcentroids[i] = initialcentroids[i][1:]
        
    return initialCentroidsIndices, initialcentroids



def main(max_iter=300):
    #Checks if we have the right amount of args
    numOfArgs = len(sys.argv)
    assert numOfArgs==4 or numOfArgs==5, "Incorrect number of arguments" 
    
    #Check if k>0 and type(k)=int
    assert isPositiveInt(sys.argv[1]), "'k' is not a positive int" 
    k = int(sys.argv[1])

    #Check if max_iter>0 and type(max_iter)=int
    #Get max_iter / file_name_1 / file_name_2
    if numOfArgs == 5:
        assert isPositiveInt(sys.argv[2]), "'max_iter' is not an positive int" 
        max_iter = int(sys.argv[2])
        file_name_1 = sys.argv[3]
        file_name_2 = sys.argv[4]
        
    else:
        file_name_1 = sys.argv[2]
        file_name_2 = sys.argv[3]
    
    
    #Read both data files and merge them
    df1 = pd.read_csv(file_name_1, header=None)
    df2 = pd.read_csv(file_name_2, header=None)
    vectors = df1.merge(df2,on=0)
    vectors.sort_values(vectors.columns[0], inplace=True)
    
    #Calculate numOfVectors=N and dimension=d
    numOfVectors = vectors.shape[0]
    dimension = vectors.shape[1]-1
    
    #Initiate the centroids list
    initialCentroidsIndices, initialcentroids = initCentroids(vectors, k, numOfVectors, dimension)
    
    #Print first row - Need to stay
    print(','.join(map(str,initialCentroidsIndices)))
    
    #mykmeanssp.fit(initialcentroids, k, max_iter, vectors, numOfVectors, dimension)
    


if __name__ == "__main__":
    main()

