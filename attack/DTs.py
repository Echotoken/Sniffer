import logging
import operator
import numpy as np
import random
import torch

def chose_data(loaddata,number, member):
    dim = loaddata.data[0].size
    data = loaddata.data.reshape(-1, dim)

    r = data.shape[0]
    f = data.shape[1]
    outdex = random.sample(list(range(r)), number)
    index = random.sample(list(range(f)), member)

    raw_pred_array, uniques = [],[]
    while True:
        if len(uniques) > 1:
            raw_data = loaddata.data[outdex]
            raw_pred = loaddata.labels[outdex]
            new_data = loaddata.data[outdex]
            break
        else:
            outdex = random.sample(list(range(r)), number)
            raw_pred_array = loaddata.labels[outdex]
            uniques = np.unique(raw_pred_array, axis=0)
           
    Shape = (number,) + loaddata.data.shape[1:]
    return index, raw_data, raw_pred, new_data, Shape


def change_data(trans_data, number, member, min, max, index, threshold):

    dim = trans_data[0].size
    trans_data = trans_data.reshape(-1, dim)

    i = 0
    for i in range(number):
        j = 0
        Lperturb = 0

        for j in range(member):
            perturb = round(random.uniform(min, max), 4)
            Lperturb = Lperturb + perturb * perturb
            if Lperturb > threshold:
                break
            trans_data[i][index[j]] = trans_data[i][index[j]] + perturb
            j += 1
        i += 1
    return trans_data


def data_proba(model, data, Shape):
    data = data.reshape(Shape)
    pred = model(data)
    if isinstance(pred, torch.Tensor):
        pred = pred.detach().numpy()
    return pred

def class_equal(raw_pred, new_pred,number):
    k = 0
    rawpred_class = []
    newpred_class = []
    while k < number:
        rawpred_class.append(np.argmax(raw_pred[k]))
        newpred_class.append(np.argmax(new_pred[k]))
        k = k + 1
    class_result = operator.eq(rawpred_class, newpred_class)
    return class_result


def DT_main(loaddata, model, number, member, min, max, threshold):
    logging.info('starting DTs Probe...')

    index, raw_data,raw_pred,new_data, Shape = chose_data(loaddata, number, member)
    logging.info(' choose {} data points: \n{}'.format(number, raw_data))
    logging.info(' min, max and threshold of the interval are {}, {}, {}'.format(min, max, threshold))

    new_data = change_data(new_data, number, member, min, max, index, threshold)
    new_pred = data_proba(model, new_data, Shape)

    loaddata.flatten_data()
    loaddata.data = np.vstack((loaddata.data, new_data))
    loaddata.labels = np.vstack((loaddata.labels, new_pred))

    if (raw_pred == new_pred).all():
        if new_pred.__contains__(1):
            logging.info(" 100% is DT (Tree or Forest).\n")
            probability = 1.
            return True, number, probability
        else:
            pred_1_list = new_pred.tolist()
            new_list = []

            for item in pred_1_list:
                if item not in new_list:
                    new_list.append(item)

            if len(new_list) == 1:
                logging.info(" 100% is not DT(Tree or Forest).\n")
                probability = 0
                return False, number, probability
            else:
                logging.info(" 100% is Forest.\n")
                probability = 1.
                return True, number, probability

    else:
        flags, i = 0, 0
        raw_pred = raw_pred.tolist()
        new_pred = new_pred.tolist()
        while i < number:
            if raw_pred[i] == new_pred[i]:
                flags = flags + 1
                i = i + 1
            else:
                i = i + 1
        probability = (flags / number)
        probab = flags / number
        if probab > 0:
            logging.info(" %.2f % confidence is DTs.\n" % ((flags / number) * 100))
            return True, number, probability
        else:
            logging.info(" 100% is not DTs.\n")
            return False, number, probability