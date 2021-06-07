import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

def main():
    iris = datasets.load_iris().data
    inertias = []
    
    for k in range(1,11):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0).fit(iris)
        inertias.append(kmeans.inertia_)
    
    plt.plot(range(1, 11), inertias)
    plt.title('Elbow Method for selection of optimal "K" clusters')
    plt.xlabel('K')
    plt.ylabel('Average Dispersion')
    
    circle_rad = 15  # This is the radius, in points
    plt.plot(3, inertias[2], 'o',
        ms=circle_rad * 2, mec='b', mfc='none', mew=2)
    plt.annotate("Elbow Point",xy=(3,inertias[2]),xytext=(4,150),
                 arrowprops=dict(arrowstyle='simple',shrinkB=circle_rad*1.2))
    
    
    plt.savefig('elbow.png')
    #plt.show()


if __name__=='__main__':
    main()
