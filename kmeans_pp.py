# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
import mykmeanssp

def isPositiveInt(s):
    try:
        i = int(s)
        return i>0 
    except:
        return False
    
    

def distance(vector1, vector2):
    '''Claculates the distance between two vectors'''
    return np.sum((vector1-vector2)**2)


def clacDi(vector, centroids, z, dimension):
    '''Calculates Di - the minimum distance of the vector from a centroid'''
    return min([distance(vector, centroids[i]) for i in range(z)])


def initCentroids(vectors, k, numOfVectors, dimension):
    assert k<numOfVectors, "The number of clusters must be smaller than the number of vectors"
    np.random.seed(0)
    
    distances = [0 for i in range(numOfVectors)]
    initialcentroids = [0 for i in range(k)]
    initialCentroidsIndices = [0 for i in range(k)]
    
    #Get the first centroid
    i = np.random.randint(0, numOfVectors+1)
    initialcentroids[0] = vectors[i]
    initialCentroidsIndices[0] = i
    
    
    z=1
    while z<k:
        for i in range(numOfVectors): #Calc Di for each vector
            distances[i] = clacDi(vectors[i], initialcentroids, z, dimension)
        
        #Calculate the probability to choose each vector as the next centroid
        sumDi = np.sum(distances)
        probabilities = distances/sumDi
        
        #Chooses the next centroid based on the probabilities we calculated
        vecInd = np.random.choice(numOfVectors,p=probabilities)
        initialcentroids[z] = vectors[int(vecInd)]
        initialCentroidsIndices[z] = int(vecInd)
        
        z+=1
    
    #Convert the initialcentroids from dataframes to simple lists
    for i in range(len(initialcentroids)):
        initialcentroids[i] = initialcentroids[i].tolist()[0]
        
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
    df1 = pd.read_csv(file_name_1, index_col=0, header=None).sort_index()
    df2 = pd.read_csv(file_name_2, index_col=0, header=None).sort_index()
    vectors = df1.merge(df2, left_index=True, right_index=True)
    vectors.index = vectors.index.astype('int64')
    
    #Calculate numOfVectors=N and dimension=d
    numOfVectors = vectors.shape[0]
    dimension = vectors.shape[1]
    
    #Initiate the centroids list
    initialCentroidsIndices, initialcentroids = initCentroids(vectors.values, k, numOfVectors, dimension)
    
    #Print first row - Need to stay
    print(','.join(map(str,initialCentroidsIndices)))
    
    mykmeanssp.fit(initialcentroids, k, max_iter, vectors, numOfVectors, dimension)
    


if __name__ == "__main__":
    main()

