# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:01:24 2017

@author: hughsalimbeni
"""


import pandas
import numpy as np



#data_path = '/Users/hughsalimbeni/Documents/dnsgpfiles/data/'
data_path = '/vol/bitbucket/hrs13/dnsgpfiles/data/'

PROPORTION_TRAIN = 0.9
SEED = 0  # change (by more than 20) for different splits


def make_split(X_full, Y_full, split):
    N = X_full.shape[0]
    n = int(N * PROPORTION_TRAIN)
    ind = np.arange(N)    
    
    np.random.seed(split + SEED) 
    np.random.shuffle(ind)
    train_ind = ind[:n]
    test_ind= ind[n:]
    
    X = X_full[train_ind]
    Xs = X_full[test_ind]
    Y = Y_full[train_ind]
    Ys = Y_full[test_ind]
    
    return X, Y, Xs, Ys

def get_mnist_data():
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets(data_path+'MNIST_data/', one_hot=False)

    X, Y = mnist.train.next_batch(mnist.train.num_examples)
    Xval, Yval = mnist.validation.next_batch(mnist.validation.num_examples)
    Xtest, Ytest = mnist.test.next_batch(mnist.test.num_examples)

    Y, Yval, Ytest = [np.array(y, dtype=int) for y in [Y, Yval, Ytest]]

    X = np.concatenate([X, Xval], 0)
    Y = np.concatenate([Y, Yval], 0)

    return X, Y, Xtest, Ytest


def get_regression_data(name, split):
    
    path = '{}{}.csv'.format(data_path, name)
    data = pandas.read_csv(path).values

    if name in ['energy', 'naval']:
        # there are two Ys for these, but take only the first
        X_full = data[:, :-2]
        Y_full = data[:, -2]
    else:
        X_full = data[:, :-1]
        Y_full = data[:, -1]
        
    
    X, Y, Xs, Ys = make_split(X_full, Y_full, split)
    
    ############# whiten inputs 
    X_mean, X_std = np.average(X, 0), np.std(X, 0)+1e-6
    
    X = (X - X_mean)/X_std
    Xs = (Xs - X_mean)/X_std
    
    return  X, Y[:, None], Xs, Ys[:, None]   





