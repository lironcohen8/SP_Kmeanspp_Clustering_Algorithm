# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def distance(vector1, vector2):
    '''Claculates the distance between two vectors'''
    dis = 0
    for i in range(vector1.shape[1]): #Runs for each dimension
        dis += (vector1.iloc[0,i]-vector2.iloc[0,i])**2 
    return dis


def clacDi(vector, centroids, z):
    '''Calculates Di - the minimum distance of the vector from a centroid'''
    minDis = distance(vector, centroids[0]) #Initiate the minimum distance to be the distance from the first centroid
    for i in range(z): #For each centroid (there are z at this point)
        dis = distance(vector, centroids[i])
        if dis < minDis:
            minDis = dis    
    return minDis


def initCentroids(vectors, k, numOfVectors, dimension):
    distances = [0 for i in range(numOfVectors)]
    centroids = []
    
    #Get the first centroid
    i = np.random.randint(0, numOfVectors+1)
    centroids.append(vectors.iloc[[i]])
    
    
    z=1
    while z<k:
        for i in range(numOfVectors): #Calc Di for each vector
            di = clacDi(vectors.iloc[[i]], centroids, z)
            distances[i] = di
        z+=1
        
        #Calculate the probability to choose each vector as the next centroid
        sumDi = np.sum(distances)
        probabilities = [distances[i]/sumDi for i in range(numOfVectors)]
        
        #Chooses the next centroid based on the probabilities we calculated
        vecInd = np.random.choice(numOfVectors,p=probabilities)
        centroids.append(vectors.iloc[[vecInd]])
    
    #Convert the centroids for dataframes to simple lists
    for i in range(len(centroids)):
        centroids[i] = centroids[i].values.tolist()[0]
        
    return centroids



def main(k=12, file_name_1='', file_name_2='', max_iter=300):
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
    dimension = vectors.shape[1]
    
    #Initiate the centroids list
    centroids = initCentroids(vectors, k, numOfVectors, dimension)
    
    print(len(centroids),centroids)
    
    






if __name__ == "__main__":
    main()

