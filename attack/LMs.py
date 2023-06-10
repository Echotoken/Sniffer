import random
import logging

import numpy as np
import pandas as pd
import torch
from sklearn import svm
from sklearn.linear_model.logistic import _multinomial_loss, _multinomial_loss_grad, safe_sparse_dot
from scipy.optimize import minimize
from sklearn.metrics import accuracy_score
from sklearn.utils.extmath import squared_norm, log_logistic
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.dummy import DummyClassifier
from utils.load_initialization_attack_pool import gen_query_set_local
import timeit


def predict_probas(X, w, intercept, multinomial=True):
    if isinstance(X, pd.DataFrame):
        X = X.values
    p = safe_sparse_dot(X, w.T, dense_output=True) + intercept

    if isinstance(p, pd.DataFrame):
        p = p.values
    p = p.ravel() if p.shape[1] == 1 else p

    p *= -1
    np.exp(p, p)
    p += 1
    np.reciprocal(p, p)

    if p.ndim == 1:
        return np.vstack([1 - p, p]).T
    else:
        p /= p.sum(axis=1).reshape((p.shape[0], -1))
        return p


def logistic_loss(w, X, Y, alpha):
    n_classes = Y.shape[1]
    n_features = X.shape[1]
    intercept = 0

    if n_classes > 2:
        fit_intercept = w.size == (n_classes * (n_features + 1))
        w = w.reshape(n_classes, -1)
        if fit_intercept:
            intercept = w[:, -1]
            w = w[:, :-1]
    else:
        fit_intercept = w.size == (n_features + 1)
        if fit_intercept:
            intercept = w[-1]
            w = w[:-1]

    z = safe_sparse_dot(X, w.T) + intercept

    if n_classes == 2:
        p = np.vstack([log_logistic(-z), log_logistic(z)]).T
    else:
        denom = expit(z)
        denom = denom.sum(axis=1).reshape((denom.shape[0], -1))
        p = log_logistic(z)
        loss = - (Y * p).sum()
        loss += np.log(denom).sum()
        loss += 0.5 * alpha * squared_norm(w)
        return loss

    loss = - (Y * p).sum() + 0.5 * alpha * squared_norm(w)
    return loss


def logistic_grad_bin(w, X, Y, alpha):
    grad = np.empty_like(w)
    n_features = X.shape[1]
    fit_intercept = w.size == (n_features + 1)

    if fit_intercept:
        intercept = w[-1]
        w = w[:-1]
    else:
        intercept = 0

    z = safe_sparse_dot(X, w.T) + intercept

    _, n_features = X.shape
    z0 = - (Y[:, 1] + (expit(-z) - 1))

    grad[:n_features] = safe_sparse_dot(X.T, z0) + alpha * w

    if fit_intercept:
        grad[-1] = z0.sum()

    return grad.flatten()


def logistic_grad(w, X, Y, alpha):

    n_classes = Y.shape[1]
    n_features = X.shape[1]
    fit_intercept = w.size == (n_classes * (n_features + 1))
    grad = np.zeros((n_classes, n_features + int(fit_intercept)))

    w = w.reshape(n_classes, -1)

    if fit_intercept:
        intercept = w[:, -1]
        w = w[:, :-1]
    else:
        intercept = 0

    z = safe_sparse_dot(X, w.T) + intercept

    denom = expit(z)
    denom = denom.sum(axis=1).reshape((denom.shape[0], -1))

    z0 = (np.reciprocal(denom) * expit(z) - Y) * expit(-z)

    grad[:, :n_features] = safe_sparse_dot(z0.T, X)
    grad[:, :n_features] += alpha * w

    if fit_intercept:
        grad[:, -1] = z0.sum(axis=0)

    return grad.ravel()



def run_opti(loss, grad, X, Y, w_dim):
    k = Y.shape[1]

    best_w = None
    best_int = None
    best_acc = 0

    alphas = [10 ** x for x in range(-16, -8)]

    for alpha in alphas:
        w0 = 1e-8 * np.random.randn(*w_dim)
        num_unknowns = len(w0.ravel())
        method = "BFGS"
        if num_unknowns >= 1000:
            method = "L-BFGS-B"
        try:
            optimLogitBFGS = minimize(loss, x0=w0,
                                        method=method,
                                        args=(X, Y, alpha),
                                        jac=grad,
                                        options={'gtol': 1e-6,
                                                'disp': True,
                                                'maxiter': 100})
            wopt = optimLogitBFGS.x
        except ValueError:
            wopt = np.zeros(w0.shape)

        if k == 2:
            wopt = wopt.reshape(1, -1)
            int_opt = wopt[0, -1]
            wopt = np.array(wopt[:, :-1])
        else:
            wopt = wopt.reshape(k, -1)
            int_opt = wopt[:, -1]
            wopt = wopt[:, :-1]

        y_true = np.argmax(Y, axis=1)
        y_pred = np.argmax(predict_probas(X, wopt, int_opt), axis=1)

        acc = accuracy_score(y_true, y_pred)
        
        if acc > 0.98:
            return acc, wopt, int_opt

        if acc >= best_acc:
            best_acc = acc
            best_w = wopt
            best_int = int_opt

    return acc, best_w, best_int



def LM_main(predictor, data, data_name):
    logging.info('starting LMs Probe...')
    quer = 0
    n = 1
    if isinstance(data.data, torch.Tensor):
        r = data.data.size()[0]
        for i in data.data.size()[1:]:
            n = n * i
    else:
        r = data.data.shape[0]
        n = data.data[0].size

    k = len(data.labels[0])
    num_unknowns = (k - int(k == 2)) * (n + 1)
    

    test_size = num_unknowns - r
    quer = 0
    data.flatten_data()
    logging.info(' needed sample nember: {}'.format(num_unknowns))
    logging.info(' current sample number in attack pool: {}'.format(r))

    if test_size > 0:
        quer += test_size

        X = gen_query_set_local(test_size, data_name)
        X = X.reshape(-1, n)
        Y = predictor(X)
       
        if isinstance(Y, torch.Tensor):
            Y = Y.detach().numpy()
        X = np.vstack((data.data, X))
        Y = np.vstack((data.labels, Y))
        data.data = X
        data.labels = Y
        logging.info(' need to query time: {}'.format(test_size))
    else:
        index = random.sample(list(range(r)), num_unknowns)
        X = data.data[index]
        Y = data.labels[index]
        logging.info(' need to query time: 0')

    if k == 2:
        wdim = (1, n + 1)
    else:
        wdim = (k, n + 1)

    X = X.reshape(-1, n)
    acc, wopt, int_opt = run_opti(logistic_loss, logistic_grad,  X, Y, wdim)

    if acc >= 0.5:
        test_query = 50
        X = gen_query_set_local(test_query, data_name)
        X = X.reshape(-1, n)
        Y = predictor(X)
       
        if isinstance(Y, torch.Tensor):
            Y = Y.detach().numpy()

        y_true = np.argmax(Y, axis=1)
        y_pred = np.argmax(predict_probas(X, wopt, int_opt), axis=1)

        data.data= np.vstack((data.data,X))
        data.labels =np.vstack((data.labels,Y))
        acc_test = accuracy_score(y_true, y_pred)

        logging.info(" {} % confidence is Linear Model.\n".format(acc_test*100))
        return True, test_size + test_query, acc_test
    else:
        logging.info(" 100% is not Linear Model.\n")
        return False, test_size, 0.