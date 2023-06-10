import numpy as np
import torch
import logging
import json

from NNs.generate_cnn import generate_nn
from NNs.matchmodel import match
from NNs.si_ni_FSGM import sinifsgm
from utils.load_initialization_attack_pool import gen_query_set_local

def stealing(predictor, shadow_model, gen_number, kl, d, device, max_epsilon):  #
    pause = False
    data = d
    blackbox_attack = sinifsgm(shadow_model, device, max_epsilon)  #
    pause, shadow_model, kl = match(data, predictor, shadow_model, blackbox_attack, kl, device, gen_number)

    return pause, kl, shadow_model 


def NN_main(predictor, data, data_name):
    if isinstance(data.data, torch.Tensor):
        r = data.data.size()[0]
    else:
        r = data.data.shape[0]
    test_query = 500 - r

    if test_query > 0:
        X = gen_query_set_local(test_query, data_name)
        Y = predictor(X)
        if isinstance(Y, torch.Tensor):
            Y = Y.detach().numpy()
        data.data= np.vstack((data.data,X))
        data.labels =np.vstack((data.labels,Y))

    device = "cuda" if torch.cuda.is_available() else "cpu"

    logging.info('starting NNs Probe...')

    before_number = data.data.shape[0]
    adv_number = 300
    gen_number = 100

    max_epsilon = 26
    if not isinstance(data.data, torch.Tensor):
        data.data = torch.tensor(data.data,requires_grad=True).to(device)

    with open("../configuration.json", "r") as f:
        json_data = json.load(f)
    number_of_substitution_model_in_NN = json_data["Local"]["number_of_substitution_model_in_NN"]
    cnn_1, cnn_2, cnn_3, FNN_1, FNN_2, FNN_3, rnn, lstm, gru = generate_nn((data.data[0].detach().numpy()).shape,data.labels.shape[1])
    if number_of_substitution_model_in_NN == 1:
        model_dict = {FNN_1:'FNN_1',rnn:'rnn',cnn_1:'cnn_1'}
    elif number_of_substitution_model_in_NN == 2:
        model_dict = {FNN_1:'FNN_1',FNN_2:'FNN_2',rnn:'rnn',lstm:'lstm',cnn_1:'cnn_1',cnn_2:'cnn_2'}
    elif number_of_substitution_model_in_NN == 3:
        model_dict = {FNN_1:'FNN_1',FNN_2:'FNN_2',FNN_3:'FNN_3',rnn:'rnn',lstm:'lstm',gru:'gru',cnn_1:'cnn_1',cnn_2:'cnn_2',cnn_3:'cnn_3'}
    
    cacc = 0.0
    racc = 0.0
    facc = 0.0
    th = 0
    for shadow_model in model_dict.keys():
        th += 1
        print(f" training {th}-th substitution model.")
        logging.info(f" training {th}-th substitution model.")
        kl = 100
        type = model_dict.get(shadow_model)

        p = False
        while kl > 0 and not p:

            total = 0
            p,  kl, shadow_model = stealing(predictor, shadow_model, gen_number, kl, data, device, max_epsilon)  #

        blackbox_attack = sinifsgm(shadow_model, device, max_epsilon)
        img, label = blackbox_attack.attack(data, shadow_model, adv_number)

        if img.shape[0] == 1:
            continue
        if not isinstance(img, torch.Tensor):
            img = torch.tensor(img, requires_grad=True).float().to(device)

        output = predictor(img)
        if isinstance(output, torch.Tensor):
            output = output.detach().numpy()
        data.data = torch.cat((data.data, img), 0)
        predic_label = np.argmax(output, axis=1)
        data.labels = np.vstack((data.labels, output))

        for (x, y) in zip(predic_label, label):
            if x != y:
                total += 1
        tacc = total / img.shape[0]

        logging.info(" local substitution {} model transfer rate: {} ".format(type, tacc))

        if type[0:3] == 'cnn':
            cacc += tacc

        elif type[0:3] == 'FNN':
            facc += tacc

        else :
            racc +=tacc

    result_dict = {cacc:'cnn', racc:'rnn', facc:'fnn'}
    seq = result_dict.get(max(cacc, racc, facc))

    logging.info('the type is {} '.format(seq))

    if isinstance(data.data, torch.Tensor):
        data.data = data.data.detach().numpy()
    query_number = data.data.shape[0] - before_number
    b_softmax = np.array([cacc,racc,facc])
    a_softmax = torch.softmax(torch.tensor(b_softmax),dim=0)

    return a_softmax, query_number