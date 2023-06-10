import numpy as np
import math


class Data_local():
    def __init__(self, shape, Predictor, dataset_name):
        self.dataset_name = dataset_name
        self.data = gen_query_set_local(shape, dataset_name)
        self.labels = Predictor(self.data)
        self.size = {"Adults":14, "cancer":30, "digits":(8,8), "fashion":(28,28), "Iris":4, "MNIST":(28,28), "CIFAR10":(3,32,32), "wine":13}[dataset_name]
    
    def flatten_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape(data_num, math.prod(self.size))
    
    def recover_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape((data_num,)+self.size)



def gen_query_set_local(shape, dataset_name):
    if dataset_name == 'Adults':
        d = np.zeros((shape, 14))
        for i in range(shape):
            d[i][0] = np.random.uniform(-1.58, 3.76)
            d[i][1] = np.random.uniform(-2.79, 3.52)
            d[i][2] = np.random.uniform(-1.66, 12.26)
            d[i][3] = np.random.uniform(-2.66, 1.21)
            d[i][4] = np.random.uniform(-3.52, 2.30)
            d[i][5] = np.random.uniform(-1.73,2.24)
            d[i][6] = np.random.uniform(-1.48,1.72)
            d[i][7] = np.random.uniform(-0.9,2.21)
            d[i][8] = np.random.uniform(-4.31,0.39)
            d[i][9] = np.random.uniform(-1.42,0.70)
            d[i][10] = np.random.uniform(-0.14,13.39)
            d[i][11] = np.random.uniform(-0.21,10.59)
            d[i][12] = np.random.uniform(-3.19,4.74)
            d[i][13] = np.random.uniform(-5.88,0.59)
    elif dataset_name == 'cancer':
        d = np.zeros((shape, 30))
        for i in range(shape):
            d[i][0] = np.random.uniform(6.98,28.11)
            d[i][1] = np.random.uniform(9.71,39.28)
            d[i][2] = np.random.uniform(43.79,188.5)
            d[i][3] = np.random.uniform(143.5,2501)
            d[i][4] = np.random.uniform(0.05,0.17)
            d[i][5] = np.random.uniform(0.01,0.35)
            d[i][6] = np.random.uniform(0.0,0.43)
            d[i][7] = np.random.uniform(0.0,0.21)
            d[i][8] = np.random.uniform(0.10,0.31)
            d[i][9] = np.random.uniform(0.04,0.1)
            d[i][10] = np.random.uniform(0.11,2.88)
            d[i][11] = np.random.uniform(0.36,4.89)
            d[i][12] = np.random.uniform(0.75,21.98)
            d[i][13] = np.random.uniform(6.8,542.2)
            d[i][14] = np.random.uniform(0.0,0.04)
            d[i][15] = np.random.uniform(0.0,0.14)
            d[i][16] = np.random.uniform(0.0,0.40)
            d[i][17] = np.random.uniform(0.0,0.53)
            d[i][18] = np.random.uniform(0.0,0.08)
            d[i][19] = np.random.uniform(0.0,0.03)
            d[i][20] = np.random.uniform(7.93,36.04)
            d[i][21] = np.random.uniform(12.02,49.54)
            d[i][22] = np.random.uniform(50.41,251.2)
            d[i][23] = np.random.uniform(185.2,4254.0)
            d[i][24] = np.random.uniform(0.07,0.23)
            d[i][25] = np.random.uniform(0.02,1.06)
            d[i][26] = np.random.uniform(0.0,1.26)
            d[i][27] = np.random.uniform(0.0,0.30)
            d[i][28] = np.random.uniform(0.15,0.67)
            d[i][29] = np.random.uniform(0.05,0.21)
    elif dataset_name == 'digits':
        d = np.zeros((shape, 8, 8))
        for i in range(shape):
            d[i] = np.random.uniform(0, 16, size=(8,8))
    elif dataset_name == 'fashion':
        d = np.zeros((shape, 28, 28))
        for i in range(shape):
            d[i] = np.random.uniform(-0.5, 0.5, size=(28,28))
    elif dataset_name == 'Iris':
        d = np.zeros((shape, 4))
        for i in range(shape):
            d[i][0] = np.random.uniform(4.3, 7.9)
            d[i][1] = np.random.uniform(2.0, 4.4)
            d[i][2] = np.random.uniform(1.0, 6.9)
            d[i][3] = np.random.uniform(0.1, 2.5)
    elif dataset_name == 'MNIST':
        d = np.zeros((shape, 28, 28))
        for i in range(shape):
            d[i] = np.random.uniform(-0.5, 0.5, size=(28, 28))
    elif dataset_name == 'CIFAR10':
        d = np.zeros((shape, 3, 32, 32))
        for i in range(shape): 
            d[i] = np.random.uniform(-0.5, 0.5, size=(3,32,32))
    elif dataset_name == 'wine':
        d = np.zeros((shape, 13))
        for i in range(shape):
            d[i][0] = np.random.uniform(11.03,14.83)
            d[i][1] = np.random.uniform(0.74,5.8)
            d[i][2] = np.random.uniform(1.36,3.23)
            d[i][3] = np.random.uniform(10.6,30.0)
            d[i][4] = np.random.uniform(70.0,162.0)
            d[i][5] = np.random.uniform(0.98,3.88)
            d[i][6] = np.random.uniform(0.34,5.08)
            d[i][7] = np.random.uniform(0.13,0.66)
            d[i][8] = np.random.uniform(0.41,3.58)
            d[i][9] = np.random.uniform(1.28,13.0)
            d[i][10] = np.random.uniform(0.48,1.71)
            d[i][11] = np.random.uniform(1.27,4.0)
            d[i][12] = np.random.uniform(278.0,1680.0)
    else:
        for i in range(shape):
            d[i] = np.random.uniform(-1.0,1.0,size=(1,))

    return d



class Data_common():
    def __init__(self, shape, predictor, dataset_name):
        self.dataset_name = dataset_name
        self.data = gen_query_set_common(shape, dataset_name)
        self.labels = predictor(self.data)
        self.size = {"Adults":14, "cancer":30, "digits":(8,8), "fashion":(28,28), "Iris":4, "MNIST":(28,28), "CIFAR10":(3,32,32), "wine":13}[dataset_name]
    
    def flatten_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape(data_num, math.prod(self.size))
    
    def recover_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape((data_num,)+self.size)


class Data_input():
    def __init__(self, shape, predictor, feature_num, feature_range):
        self.data, self.size = gen_query_set_input(shape, feature_num, feature_range)
        self.labels = predictor(self.data)
    
    def flatten_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape(data_num, math.prod(self.size[1:]))
    
    def recover_data(self):
        if not isinstance(self.size, int):
            data_num = self.data.shape[0]
            self.data = self.data.reshape((data_num,)+ self.size)


def gen_query_set_input(shape, feature_num, feature_range):

    if "all" in feature_range:
        feature_range = feature_range.replace("all", "")

        list1 = feature_range.split(',')
        list2 = []
        for j in list1[:-1]:
            list2.append(float(j))
        f_range = np.array(list2)

        list1 = feature_num.split(',')
        list2 = []
        for j in list1:
            list2.append(int(j))

        d = np.random.uniform(f_range[0], f_range[1], size=((shape,) + tuple(list2)))
    else:
        list1 = feature_range.split(',')
        list2 = []
        for j in list1[:-1]:
            list2.append(float(j))
        f_range = np.array(list2)

        list1 = feature_num.split(',')
        list2 = []
        for j in list1:
            list2.append(int(j))

        d = np.zeros((shape,) + tuple(list2))
        num = 0 
        for i in range(shape):
            for j in range(math.prod(tuple(list2))):
                d[i][j] = np.random.uniform(f_range[num], f_range[num+1])
                num += 2
            num = 0
    return d, ((shape,) + tuple(list2))

def gen_query_set_common(shape, dataset_name):

    if dataset_name == 'Adults':
        d = np.zeros((shape, 14))
        for i in range(shape):
            d[i][0] = np.random.uniform(-1.58, 3.76)
            d[i][1] = np.random.uniform(-2.79, 3.52)
            d[i][2] = np.random.uniform(-1.66, 12.26)
            d[i][3] = np.random.uniform(-2.66, 1.21)
            d[i][4] = np.random.uniform(-3.52, 2.30)
            d[i][5] = np.random.uniform(-1.73,2.24)
            d[i][6] = np.random.uniform(-1.48,1.72)
            d[i][7] = np.random.uniform(-0.9,2.21)
            d[i][8] = np.random.uniform(-4.31,0.39)
            d[i][9] = np.random.uniform(-1.42,0.70)
            d[i][10] = np.random.uniform(-0.14,13.39)
            d[i][11] = np.random.uniform(-0.21,10.59)
            d[i][12] = np.random.uniform(-3.19,4.74)
            d[i][13] = np.random.uniform(-5.88,0.59)
    elif dataset_name == 'cancer':
        d = np.zeros((shape, 30))
        for i in range(shape):
            d[i][0] = np.random.uniform(6.98,28.11)
            d[i][1] = np.random.uniform(9.71,39.28)
            d[i][2] = np.random.uniform(43.79,188.5)
            d[i][3] = np.random.uniform(143.5,2501)
            d[i][4] = np.random.uniform(0.05,0.17)
            d[i][5] = np.random.uniform(0.01,0.35)
            d[i][6] = np.random.uniform(0.0,0.43)
            d[i][7] = np.random.uniform(0.0,0.21)
            d[i][8] = np.random.uniform(0.10,0.31)
            d[i][9] = np.random.uniform(0.04,0.1)
            d[i][10] = np.random.uniform(0.11,2.88)
            d[i][11] = np.random.uniform(0.36,4.89)
            d[i][12] = np.random.uniform(0.75,21.98)
            d[i][13] = np.random.uniform(6.8,542.2)
            d[i][14] = np.random.uniform(0.0,0.04)
            d[i][15] = np.random.uniform(0.0,0.14)
            d[i][16] = np.random.uniform(0.0,0.40)
            d[i][17] = np.random.uniform(0.0,0.53)
            d[i][18] = np.random.uniform(0.0,0.08)
            d[i][19] = np.random.uniform(0.0,0.03)
            d[i][20] = np.random.uniform(7.93,36.04)
            d[i][21] = np.random.uniform(12.02,49.54)
            d[i][22] = np.random.uniform(50.41,251.2)
            d[i][23] = np.random.uniform(185.2,4254.0)
            d[i][24] = np.random.uniform(0.07,0.23)
            d[i][25] = np.random.uniform(0.02,1.06)
            d[i][26] = np.random.uniform(0.0,1.26)
            d[i][27] = np.random.uniform(0.0,0.30)
            d[i][28] = np.random.uniform(0.15,0.67)
            d[i][29] = np.random.uniform(0.05,0.21)
    elif dataset_name == 'digits':
        d = np.zeros((shape, 64))
        for i in range(shape):
            d[i] = np.random.uniform(0, 16, size=64)
    elif dataset_name == 'fashion':
        d = np.zeros((shape, 784))
        for i in range(shape):
            d[i] = np.random.uniform(-0.5, 0.5, size=784)
    elif dataset_name == 'Iris':
        d = np.zeros((shape, 4))
        for i in range(shape):
            d[i][0] = np.random.uniform(4.3, 7.9)
            d[i][1] = np.random.uniform(2.0, 4.4)
            d[i][2] = np.random.uniform(1.0, 6.9)
            d[i][3] = np.random.uniform(0.1, 2.5)
    elif dataset_name == 'MNIST':
        d = np.zeros((shape, 784))
        for i in range(shape):
            d[i] = np.random.uniform(-0.5, 0.5, size=784)
    elif dataset_name == 'CIFAR10':
        d = np.zeros((shape, 3072))
        for i in range(shape):
            d[i] = np.random.uniform(-0.5, 0.5, size=3072)
    elif dataset_name == 'wine':
        d = np.zeros((shape, 13))
        for i in range(shape):
            d[i][0] = np.random.uniform(11.03,14.83)
            d[i][1] = np.random.uniform(0.74,5.8)
            d[i][2] = np.random.uniform(1.36,3.23)
            d[i][3] = np.random.uniform(10.6,30.0)
            d[i][4] = np.random.uniform(70.0,162.0)
            d[i][5] = np.random.uniform(0.98,3.88)
            d[i][6] = np.random.uniform(0.34,5.08)
            d[i][7] = np.random.uniform(0.13,0.66)
            d[i][8] = np.random.uniform(0.41,3.58)
            d[i][9] = np.random.uniform(1.28,13.0)
            d[i][10] = np.random.uniform(0.48,1.71)
            d[i][11] = np.random.uniform(1.27,4.0)
            d[i][12] = np.random.uniform(278.0,1680.0)
    else:
        for i in range(shape):
            d[i] = np.random.uniform(-1.0,1.0,size=(1,))

    return d