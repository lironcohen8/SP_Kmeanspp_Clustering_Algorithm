#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>
#include <assert.h>


int k, max_iter, dimension, numOfVectors = 0, changes = 1;
float rawK, rawMaxIter;
double **vectors, **centroids;
int **clusters, *clustersSizes;

void *calloc(size_t nitems, size_t size);
void *malloc(size_t size);
void *realloc(void *ptr, size_t size);
void free(void *ptr);
char *strtok(char * str, const char *delim);
double atof(const char * str);

void assignVectorToCluster();
void updateCentroidValue();
void printResult();

static struct PyModuleDef mykmeanssp = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp",     // name of module exposed to Python
    "mykmeanssp Python wrapper for custom C extension library.", // module documentation
    -1
};

static PyObject* fit(PyObject *self, PyObject *args){
    int counter = 1;
    if (!PyArg_ParseTuple(args,"O",&centroids, &k, &max_iter, &vectors, &numOfVectors, &dimension)){
        return NULL;
    }

    clusters = (int **)calloc(k, numOfVectors*sizeof(int));
    assert(clusters != NULL);
    while ((counter<=max_iter) && (changes > 0)) {
        assignVectorToCluster();
        updateCentroidValue();
        counter += 1;
    }

    printResult();
    free(vectors);
    free(centroids);
    free(clusters);
    free(clustersSizes);
}










int calcDimension(char buffer[]) {
    /*
    gets a buffer contains the first vector and calculates 
    */
    int i, dimension; 
    char c;
    dimension = 0;
    i = 0;
    c = buffer[i];
    while (c != '\n') {
        if (c == ',') {
            dimension++;
        }
        c = buffer[++i];
    }
    buffer[i] = '\0';
    return dimension+1;
}

void readFile() {
    /*Reading the input file and put the data into the 'vectors' list*/
    int j, sizeFull = 1;
    char *vectorStr, buffer[1000];
    double **tmp;
    vectorStr = (char *)calloc(dimension, 100*sizeof(char));
    assert(vectorStr != NULL);
    vectors = (double **)malloc(1 * sizeof(*vectors));
    assert(vectors != NULL);
    fgets(buffer,1000,stdin);
    dimension = calcDimension(buffer);
    do {
        if (numOfVectors == sizeFull) {
            sizeFull *= 2;
            tmp = realloc(vectors, sizeFull * sizeof(*vectors));
            vectors = tmp;
        }
        vectorStr = strtok(buffer, ",");
        j = 0;
        vectors[numOfVectors] = (double *)calloc(dimension, sizeof(double)); 
        assert(vectors[numOfVectors] != NULL);
        while (vectorStr != NULL) {
            vectors[numOfVectors][j] = atof(vectorStr);
            vectorStr = strtok(NULL, ",");
            j++;
        }
        numOfVectors++;
    }
    while (fgets(buffer,1000,stdin) != NULL);
    free(vectorStr);
}

void initCentroids() {
    /*Initialize the clusters and their centroids from the first K vectors*/
    int i,j;
    centroids = (double **)calloc(k, dimension*sizeof(double));
    assert(centroids != NULL);
    assert(k < numOfVectors);
    for (i = 0; i < k; i++) {
        centroids[i] = (double *)calloc(dimension, sizeof(double)); 
        assert(centroids[i] != NULL);
        for (j = 0; j < dimension; j++) {
            centroids[i][j] = vectors[i][j];
        }
    }
}

double distance(double *vector1, double *vector2) {
    /*'''Claculates the distance between two vectors*/
    double dis = 0;
    int i;
    for (i = 0; i < dimension; i++) {
        dis += (vector1[i]-vector2[i])*(vector1[i]-vector2[i]);
    }
    return dis;
}

int closestCentroid(double *vector) {
    /*Finds the closest centroid to a vector by the distance function*/
    double minDis, dis;
    int minCenInd,i;
    
    minDis = distance(vector, centroids[0]); /*Initiate the minimum distance to be the distance from the first centroid*/
    minCenInd = 0; /*Initiate the closest centroid to be the first one*/
    
    for (i = 0; i < k; i++) { /*For each centroid (there are K)*/
        dis = distance(vector, centroids[i]);
        if (dis < minDis) {
            minDis = dis;
            minCenInd = i;
        }
    }   
    return minCenInd;
}
 
void assignVectorToCluster() {
    /*Finds the closest centroid for each vector and adds
    the vector to the centroids cluster*/
    int i, newCentroidInd, clusterSize;
    int * cluster;
    clustersSizes = (int *)calloc(k, sizeof(int));
    assert(clustersSizes != NULL);

    /*Clearing all clusters (we do not want to remember what was here)*/
    for (i = 0; i < k; i++) { 
        clusters[i] = (int *)calloc(numOfVectors, sizeof(int));
        assert(clusters[i] != NULL);
    }
        
    for (i = 0; i < numOfVectors; i++) {
        newCentroidInd = closestCentroid(vectors[i]); /*Finds the closest centroid*/
        cluster = clusters[newCentroidInd];
        clusterSize = clustersSizes[newCentroidInd];
        cluster[clusterSize] = i; /*Adds the vector to the appropriate cluster*/
        clustersSizes[newCentroidInd]++;
    }
}

double* calcCentroidForCluster(int clusterInd) {
    /*Calculates the centroid for a given cluster*/
    int numOfVectorsInCluster, i, j;
    int * cluster;
    double * sumVector = (double *)calloc(dimension, sizeof(double));
    assert(sumVector != NULL);
    numOfVectorsInCluster = clustersSizes[clusterInd];
    cluster = clusters[clusterInd];
    
    for (i = 0; i < dimension; i++) {
        for (j = 0; j < numOfVectorsInCluster; j++) {
            sumVector[i] += (vectors[cluster[j]])[i];
        }
    }

    for (i = 0; i < dimension; i++) {
        sumVector[i] /= numOfVectorsInCluster; /*Replace the sum with the average*/
    }
    return sumVector;
}

void updateCentroidValue() {
    /*Updates the centroid value for each cluster and checks if 
    it is different then what we had before*/
    int i, j;
    double * newValue;
    changes = 0;
    for (i = 0; i < k; i++) {
        newValue = calcCentroidForCluster(i);
        for (j = 0; j < dimension; j++) {
            if (newValue[j] != centroids[i][j]) { /*If the centroid changed*/
                changes += 1;
            }    
            centroids[i][j] = newValue[j];
        }
    }
}

void printResult() {
    /*Prints the centroids*/
    int i, j;
    for (i = 0; i < k; i++) {
        for (j = 0; j < dimension; j++) {
            printf("%.4f", centroids[i][j]); /*Format the floats precision to 4 digits*/
            if (j < dimension - 1) {
                printf(",");
            }
        }
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    int counter = 1;
    assert(argc == 3 || argc == 2); /*Checks if we have the right amount of args*/

    assert(sscanf(argv[1], "%f", &rawK) == 1);
    k = (int)rawK;
    assert(rawK - k == 0 && k > 0); /*checks if k is a positive int*/

    max_iter = 200;
    if (argc == 3) {
        assert(sscanf(argv[2], "%f", &rawMaxIter) == 1);
        max_iter = (int)rawMaxIter;
        assert(rawMaxIter - max_iter == 0 && max_iter > 0); /*checks if max_iter is a positive int*/
    }
    
    readFile();
    initCentroids();
    
    clusters = (int **)calloc(k, numOfVectors*sizeof(int));
    assert(clusters != NULL);
    while ((counter<=max_iter) && (changes > 0)) {
        assignVectorToCluster();
        updateCentroidValue();
        counter += 1;
    }

    printResult();
    free(vectors);
    free(centroids);
    free(clusters);
    free(clustersSizes);
    return 0;
}