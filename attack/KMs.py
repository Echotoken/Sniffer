import numpy as np
import logging
import torch
import random as rand


def set_parameter(dim):
    
    test_time = 10
    max_change_dim = dim
    basic_change_input = 100000
    max_change_input = 50000
    logging.info(' initialize %d data points, huge nember: %d.' % (test_time, basic_change_input))
    return test_time, max_change_dim, basic_change_input, max_change_input

def gen_query_set(shape):
    d=np.zeros(shape)
    for i in range(shape[0]):
        d[i] = np.random.uniform(-1, 1,size=shape[1:])
    return d


def get_result(dim,userdata, test_time, max_change_dim, basic_change, max_change, predictor):
    inputdata = userdata.copy()
    n = inputdata.shape[0]

    if n < test_time:
        new_shape = (test_time - n,) + inputdata.shape[1:]
        zero_inputdata = np.zeros(new_shape)
        inputdata = np.vstack((inputdata, zero_inputdata))
        n = test_time
    elif n > test_time:
        inputdata=inputdata[0:test_time]
        n = test_time
        
    ori_shape = inputdata.shape

    inputdata = inputdata.reshape(n, -1)
    for i in range(test_time):
        for j in range(max_change_dim):
            k = rand.randint(0, dim - 1)
            inputdata[i][k] = rand.randint(0, max_change) + basic_change

    inputdata=inputdata.reshape(ori_shape)

    logging.info(' query data points:\n%s' % inputdata)

    result = predictor(inputdata)

    logging.info(' confidence of the above data points:\n%s' % result)

    return result, test_time

def judge(result,test_time):
    dif = []
    lim_01 = 0.0000000000000001
    lim_dif = 0.2
    lim_same = 0.000000000001
    if isinstance(result,torch.Tensor):
        result = result.deach().numpy()
    result.reshape(test_time,-1)

    for x in result.reshape(-1, ):
        if abs(x-0) < lim_01 or abs(x-1) < lim_01:
            logging.info(" confidence has 1. or 0., 100% is not KMs.")
            return 1, 0.

    for i in range(test_time - 1):
        for j in range(test_time-i-1):
            dif.append(np.linalg.norm(result[i]-result[test_time-j-1]))

    dif_item = 0
    close_item = 0
    for x in dif:
        if x > lim_same:
            if x > lim_dif:
                dif_item += 1
            else:
                close_item += 1

    if not (dif_item and close_item):
        return True, 1.
    else:
        return False, 0.

def adjust_parameter(dim, userdata, basic_change, max_change, predictor):
    inputdata = userdata.copy()
    n = inputdata.shape[0]
    adjust_time = 0
    test_time = 2

    if n < test_time:
        new_shape = (test_time - n,) + inputdata.shape[1:]
        zero_inputdata = np.zeros(new_shape)
        inputdata = np.vstack((inputdata, zero_inputdata))
        n = test_time
    elif n > test_time:
        inputdata = inputdata[0: test_time]
        n = test_time
    ori_shape = inputdata.shape
    inputdata = inputdata.reshape(n, -1)

    for j in range(1, test_time):
        for i in range(dim):
            inputdata[j][i] = inputdata[0][i]

    k = rand.randint(0, dim - 1)
    for i in range(test_time):
        inputdata[i][k] = rand.randint(0, max_change) + basic_change
    inputdata = inputdata.reshape(ori_shape)
    logging.info(' data points after adding huge number:\n%s' % inputdata)
    result = predictor(inputdata)
    logging.info(' confidence of the above data points:\n %s ' % result)
    adjust_time += test_time

    dif = []
    if isinstance(result,torch.Tensor):
        result = result.deach().numpy()
    result.reshape(test_time,-1)
    for x in result.reshape(-1, ):
        if abs(x-0)<0.00001 or abs(x-1)<0.00001:
            return 1, basic_change, max_change, adjust_time

    for i in range(test_time - 1):
        for j in range(test_time-i-1):
            dif.append(np.linalg.norm(result[i]-result[test_time-j-1]))

    for x in dif:
        if x > 0.000001:
            logging.info(' huge number maybe small.')
            return 0, basic_change, max_change, adjust_time

    logging.info(' huge number is enough.')
    return 2, basic_change, max_change, adjust_time

def KM_main(userdata, predictor):

    logging.info('starting KMs Probe...')
    
    dim = 1
    if isinstance(userdata, torch.Tensor):
        for i in userdata.size()[1:]:
            dim = dim * i
    else:
        dim = userdata[0].size
        
    test_time, max_change_dim, basic_change, max_change = set_parameter(dim)

    query_time = 0
    adjust_time = 3
    adjust_temp = 0
    is_adjust = 0
    while(is_adjust==0 and adjust_temp < adjust_time):
        logging.info(' adjust huge number {} times.'.format(adjust_temp+1))
        is_adjust, basic_change, max_change, adjust_test_time = adjust_parameter(dim, userdata, basic_change, max_change, predictor)
        query_time += adjust_test_time
        adjust_temp += 1

    if is_adjust == 1:
        logging.info(" confidence has 1. or 0., 100% is not KMs.\n")
        return False, 0., query_time
    if is_adjust == 0:
        logging.info(" adjust time is enough, 100% is not KMs.\n")
        return False, 0., query_time

    result, test_time = get_result(dim, userdata, test_time, max_change_dim, basic_change, max_change, predictor)
    judge_result, judge_proba = judge(result, test_time)

    if judge_result:
        logging.info(" {}% is KMs.\n".format(np.around(judge_proba * 100, 2)))
        return True, judge_proba, test_time + query_time
    else:
        logging.info(" {}% is not KMs.\n".format(np.around(judge_proba * 100, 2)))
        return False, judge_proba, test_time + query_time