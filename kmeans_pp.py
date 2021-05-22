# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

global centroids 
centroids = []

global distances
distances = []

global probabilities
probabilities = []




def distance(vector1, vector2):
    dis = 0
    for i in range(vector1.shape[1]): #Runs for each dimension
        dis += (vector1.iloc[0,i]-vector2.iloc[0,i])**2 
    return dis

def clacDi(vector, z):
    minDis = distance(vector, centroids[0]) #Initiate the minimum distance to be the distance from the first centroid
    for i in range(z): #For each centroid (there are K)
        dis = distance(vector, centroids[i])
        if dis < minDis:
            minDis = dis
            
    return minDis





def main(k=3, file_name_1='', file_name_2='', max_iter=300):
    global distances
    global probabilities
    file_name_1 = r'C:\Users\shake\OneDrive\אוניברסיטה\סמסטר ד\פרויקט תוכנה\projects\SoftwareProjectEx2\tests\test_data\input_1_db_1.txt'
    file_name_2 = r'C:\Users\shake\OneDrive\אוניברסיטה\סמסטר ד\פרויקט תוכנה\projects\SoftwareProjectEx2\tests\test_data\input_1_db_2.txt'
    max_iter = 333
    
    df1 = pd.read_csv(file_name_1, header=None)
    df2 = pd.read_csv(file_name_2, header=None)
    df1 = df1.merge(df2,on=0)
    numOfVectors = df1.shape[0]
    distances = [0 for i in range(numOfVectors)]
    dimension = df1.shape[1]
    
    i = np.random.randint(0, numOfVectors+1)
    centroids.append(df1.iloc[[i]])
    
    
    z=1
    while z<k:
        for i in range(numOfVectors):
            di = clacDi(df1.iloc[[i]], z)
            distances[i] = di
        z+=1
        sumDi = np.sum(distances)
        probabilities = [distances[i]/sumDi for i in range(numOfVectors)]
        vecInd = np.random.choice(numOfVectors,p=probabilities)
        centroids.append(df1.iloc[[vecInd]]) 
        
    print(centroids)
    
    






if __name__ == "__main__":
    main()

