import csv
import matplotlib.pyplot as plt
import numpy as np
import math

def read_csv_file():
    """
    This  def is for reading fom file and geting all data 
    """
    dataset = csv.DictReader(open("dataset.csv"))
    X_set =[]
    lable_set = []
    for row in dataset:
        X_set.append((float(row.get('X1')), float(row.get('X2'))))
        lable_set.append(row.get('Label'))
    return X_set, lable_set

def split_train_test(input_set, lable_set, persent):
    """
    This def is for spliting data to training and testing data accourding to persent that is taken
    """
    number_of_training_inputs = int(len(input_set) * persent)
    training_inputs = input_set[:number_of_training_inputs]
    testing_inputs = input_set[number_of_training_inputs:]
    training_lables = lable_set[:number_of_training_inputs]
    testing_lables = lable_set[number_of_training_inputs:]
    return training_inputs, training_lables, testing_inputs, testing_lables

def show_scatter(X_set1, label_set1, title1, X_set2, label_set2, title2):
    """
    This def is for showing scatter diagram
    """
    fig, diagram = plt.subplots(1, 2)
    fig.set_size_inches(10, 4)
    X0_set1 = []
    X1_set1 = []
    for i in range(len(label_set1)):
        if label_set1[i] == '0':
            X0_set1.append(X_set1[i])
        else:
            X1_set1.append(X_set1[i])
    diagram[0].scatter([X[0] for X in X0_set1], [X[1] for X in X0_set1], color='r', Label='label=0')
    diagram[0].scatter([X[0] for X in X1_set1], [X[1] for X in X1_set1], color='b', label='label=1')
    diagram[0].set_xlabel('X0')
    diagram[0].set_ylabel('X1')
    diagram[0].set_title(title1)
    diagram[0].legend()
    X0_set2 = []
    X1_set2 = []
    for i in range(len(label_set2)):
        if label_set2[i] == '0':
            X0_set2.append(X_set2[i])
        else:
            X1_set2.append(X_set2[i])
    diagram[1].scatter([X[0] for X in X0_set2], [X[1] for X in X0_set2], color='r', Label='label=0')
    diagram[1].scatter([X[0] for X in X1_set2], [X[1] for X in X1_set2], color='b', label='label=1')
    diagram[1].set_xlabel('X0')
    diagram[1].set_ylabel('X1')
    diagram[1].set_title(title2)
    diagram[1].legend()
    plt.show()


def sigmiod_function(input):
    output = 1.0/(1.0+math.exp(-input))
    return output

def compute_grade1(X, y0, W, b):
    """
    This def is for computing gradient and cost for one layer neural network
    and after computing it returns cost and gradient 
    """
    u = np.dot(X, W) + b
    y = sigmiod_function(u)
    cost = -(y0 * math.log2(y) + (1 - y0) * math.log2(1 - y))
    dcost_dy = -(y0 * (1.0 / y ) - (1 - y0) * (1.0 / (1 - y)))
    dy_du = sigmiod_function(u) * (1 - sigmiod_function(u))
    du_dW = X
    du_db = 1

    dcost_dW = np.multiply(dcost_dy * dy_du, du_dW)
    dcost_db = dcost_dy * dy_du * du_db
    return dcost_dW, dcost_db, cost

def training1(training_inputs, training_lables):
    """
    This def is for training data in one layer neural network
    after training it returns W and b
    """
    W = np.random.normal(0, 1, 2)
    b = np.random.normal(0, 1, 1)
    n_epoch = 1000
    lr = 35
    for i in range(n_epoch):
        dcost_dW = 0
        dcost_db = 0
        cost = 0
        for k in range(len(training_inputs)):
            X = training_inputs[k]
            y0 = training_lables[k]
            dW, db, c = compute_grade1(X, int(y0), list(W), b)
            dcost_dW += dW
            dcost_db += db
            cost += c
        print('cost in epoch {}: {}'.format(i, cost))
        W = W - lr * dcost_dW / len(training_inputs)
        b = b - lr * dcost_db / len(training_inputs)
    return W, b
def predict_test_data1(testing_inputs, testing_labels, W, b):
    number_of_true = 0
    predicted_out = []
    for i in range(len(testing_inputs)):
        X = testing_inputs[i]
        u = np.dot(X, W) + b
        y = sigmiod_function(u)
        if y >= 0.5:
            lable = '1'
        else:
            lable = '0'
        predicted_out.append(lable)
        if lable == testing_labels[i]:
            number_of_true += 1
    accuarcy = number_of_true / len(testing_inputs)
    print("#################")
    print('accuracy in test: ' + str(accuarcy))
    show_scatter(testing_inputs, testing_labels, 'testing data', testing_inputs, predicted_out, 'predicted (accuarcy={})'.format(accuarcy))
    return accuarcy

def compute_grade2(X, y0, W, V, U, B):
    """
    This def is for computing gradient and cost for tow layers neural network
    and after computing it returns cost and gradient 
    """
    s1 = np.dot(X, W) + B[0]
    z0 = sigmiod_function(s1)
    s2 = np.dot(X, V) + B[1]
    z1 = sigmiod_function(s2)
    Z = [z0, z1]
    s3 = np.dot(Z, U) + B[2]
    y = sigmiod_function(s3)
    cost = (y - y0) ** 2 

    dcost_dy = 2 * (y - y0)
    dy_ds3 = y * (1 - y)
    dZ1_ds2 = z1 * (1 - z1)
    dZ0_ds1 = z0 * (1 - z0)

    dcost_dU = np.multiply(dcost_dy * dy_ds3, Z)
    dcost_dV = np.multiply(dcost_dy * dy_ds3 * U[1] * dZ1_ds2, X)
    dcost_dW = np.multiply(dcost_dy * dy_ds3 * U[0] * dZ0_ds1, X)
    dcost_db0 = dcost_dy * dy_ds3 * U[0] * dZ0_ds1 * 1.0
    dcost_db1 = dcost_dy * dy_ds3 * U[1] * dZ1_ds2 * 1.0
    dcost_db2 = dcost_dy * dy_ds3 * 1.0

    return dcost_dW, dcost_dV, dcost_dU, dcost_db0, dcost_db1, dcost_db2, cost


def training2(training_inputs, training_labels):
    """
    This def is for training data in tow layers neural network
    after training it returns W, V, Z and b
    """

    W = np.random.normal(0, 1, 2)
    V = np.random.normal(0, 1, 2)
    U = np.random.normal(0, 1, 2)
    b0 = np.random.normal(0, 1, 1)
    b1 = np.random.normal(0, 1, 1)
    b2 = np.random.normal(0, 1, 1)
    n_epoch = 1000
    lr = 0.3
    trains = list(zip(training_inputs, training_labels))
    for i in range(n_epoch):
        cost = 0
        np.random.shuffle(trains)
        for k in range(len(trains)):
            X = trains[k][0]
            y0 = trains[k][1]
            dW, dV, dU, db0, db1, db2, c = compute_grade2(X, int(y0), list(W), list(V), list(U), [b0, b1, b2])
            W -= (lr * dW)
            V -= (lr * dV)
            U -= (lr * dU)
            b0 -= (lr * db0)
            b1 -= (lr * db1)
            b2 -= (lr * db2)
            cost += c
        print('cost in epoch {}: {}'.format(i, cost))
    return W, V, U, b0, b1, b2, cost


def predict_test_data2(testing_inputs, testing_labels, W, V, U, b0, b1, b2):
    """
    This def is for predict result of test data and compare to lable of this data
    after that we show the 
    """

    number_of_true = 0
    predicted_out = []
    for i in range(len(testing_inputs)):
        X = testing_inputs[i]
        s1 = np.dot(X, W) + b0
        z0 = sigmiod_function(s1)
        s2 = np.dot(X, V) + b1
        z1 = sigmiod_function(s2)
        Z = [z0, z1]
        s3 = np.dot(Z, U) + b2
        y = sigmiod_function(s3)
        if y >= 0.5:
            lable = '1'
        else:
            lable = '0'
        predicted_out.append(lable)
        if lable == testing_labels[i]:
            number_of_true += 1
    accuarcy = number_of_true / len(testing_inputs)
    print("#################")
    print('accuracy in test: ' + str(accuarcy))
    show_scatter(testing_inputs, testing_labels, 'testing data', testing_inputs, predicted_out, 'predicted (accuarcy={})'.format(accuarcy))
    return accuarcy

if __name__ == "__main__":
    """
    Getting and scattering data
    """
    X_set, lable_set = read_csv_file()
    training_inputs, training_lables, testing_inputs, testing_lables = split_train_test( X_set, lable_set, 0.8 )
    """
    Part 1: one layer neural network 
    """
    # show_scatter(training_inputs, training_lables, 'training data', testing_inputs, testing_lables, 'testing data')
    # W1, b1 = training1(training_inputs, training_lables)
    # predict_test_data1(testing_inputs, testing_lables, W1, b1)

    """
    Part 2: tow layers neural network
    """
    W, V, U, b0, b1, b2, cost = training2(training_inputs, training_lables)
    predict_test_data2(testing_inputs, testing_lables, W, V, U, b0, b1, b2)

    """
    folowing part is for run test part 10 times and computing average of accuracy
    because of using stochastic gradient descent we shaffel data and need to compute the average
    """
    # sum_accuracy = 0
    # for i in range(10):
    #     W, V, U, b0, b1, b2, cost = training2(training_inputs, training_lables)
    #     accuarcy = predict_test_data2(testing_inputs, testing_lables, W, V, U, b0, b1, b2,)
    #     sum_accuracy += accuarcy
    # avg_accuracy = sum_accuracy / 10
    # print("average of accuracy in 10 time testing: {}".format(avg_accuracy))
