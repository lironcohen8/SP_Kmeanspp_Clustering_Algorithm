# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


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



def main(k=3, file_name_1='', file_name_2='', max_iter=300):
    #NEEDS TO GO!!!
    file_name_1 = r'C:\Users\shake\OneDrive\אוניברסיטה\סמסטר ד\פרויקט תוכנה\projects\SoftwareProjectEx2\tests\test_data\input_1_db_1.txt'
    file_name_2 = r'C:\Users\shake\OneDrive\אוניברסיטה\סמסטר ד\פרויקט תוכנה\projects\SoftwareProjectEx2\tests\test_data\input_1_db_2.txt'
    #NEEDS TO GO!!!
    
    #Read both data files and merge them
    df1 = pd.read_csv(file_name_1, header=None)
    df2 = pd.read_csv(file_name_2, header=None)
    vectors = df1.merge(df2,on=0)
    
    #Calculate numOfVectors=N and dimension=d
    numOfVectors = vectors.shape[0]
    dimension = vectors.shape[1]-1
    
    #Initiate the centroids list
    initialCentroidsIndices, initialcentroids = initCentroids(vectors, k, numOfVectors, dimension)
    
    print(len(initialcentroids),initialCentroidsIndices, initialcentroids)
    
    






if __name__ == "__main__":
    main()

