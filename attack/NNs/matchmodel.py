import numpy as np
import random
import logging
from torch.utils.data import DataLoader, TensorDataset
import torch
import torch.optim as optim
from numpy import argmax
import torch.nn as nn
import NNs.Utils as util
import torch.nn.functional as F


def match(data, target_model, model, attack, kl_o, device, gen_number):
    pause = False
    learning_rate = 0.001
    epechos = 3
    batch_size = 32

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.KLDivLoss(reduction='batchmean')

    if data.data.shape[0] < 5000:
        logging.info("generate AE ")
        all_orig_img, all_target_labels, all_orig_labels, all_orig_img_id = util.generate_generation_data_set(data, gen_number, 0)
        
        i = 0
        lp = gen_number
        while (i < lp):
            orig_img = all_orig_img[i:i + 1]
            target = all_target_labels[i:i + 1]
            
            adv_img = attack.generation(orig_img, target, model)

            if not isinstance(adv_img, torch.Tensor):
                adv_img = torch.tensor(adv_img,requires_grad=True).float()
            data.data = torch.cat((data.data, adv_img),0)
            target_out = target_model(adv_img)
            if isinstance(target_out,torch.Tensor):
                target_out = target_out.detach().numpy()
            data.labels = np.vstack((data.labels, target_out))
            i += 1

    dataset = TensorDataset(data.data, torch.tensor(data.labels))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    kl, model = train(model, dataloader, epechos, device, criterion, batch_size, optimizer)
    if kl_o - kl < 0.05 :
        pause = True
    return pause, model, kl


def weights_init(model):
    for m in model.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.xavier_normal_(m.weight.data)
        elif isinstance(m, nn.Linear):
            m.weight.data.normal_()


def train(model, dataloader, epechos, device, criterion, batch_size, optimizer):
    logging.info(" train shadow model")
    kl = 0
    for epoch in range(epechos):
        running_loss = 0.0
        running_acc = 0.0
        i = 1
        for j, (inputs, labels) in enumerate(dataloader):
            optimizer.zero_grad()
            labels = labels.float().to(device)
            inputs = inputs.to(device)
            outputs = model(inputs.float())
            if torch.sum(labels[0,1])!=1 :
                loss = criterion(F.log_softmax(outputs), F.softmax(labels))
            else:
                loss = criterion(F.log_softmax(outputs), labels)
            loss.backward(retain_graph=True)
            acc = np.mean(argmax(outputs.detach().numpy(), 1) == argmax(labels.detach().numpy(), 1))
            optimizer.step()
            running_loss += loss.data.item()
            running_acc += acc
            i += 1
        kl += running_loss / (i - 1)
    kl = kl / epechos
    return kl, model

def pre_train(model, data, epechos, device, criterion, batch_size, optimizer):
    dataset = TensorDataset(data.data, torch.tensor(data.labels))
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    for epoch in range(epechos):
        running_loss = 0.0
        running_acc = 0.0
        i = 1
        for j, (inputs, labels) in enumerate(dataloader):
            optimizer.zero_grad()
            labels = labels.float().to(device)
            inputs = inputs.to(device)
            outputs = model(inputs.float())
            if torch.sum(labels[0,1])!=1 :
                loss = criterion(F.log_softmax(outputs), F.softmax(labels))
            else:
                loss = criterion(F.log_softmax(outputs), labels)
            loss.backward(retain_graph=True)
            if isinstance(outputs,torch.Tensor):
                acc = np.mean(argmax(outputs.detach().numpy(), 1) == argmax(labels.detach().numpy(), 1))
            else:
                acc = np.mean(argmax(outputs, 1) == argmax(labels.detach().numpy(), 1))
            optimizer.step()
            running_loss += loss.data.item()
            running_acc += acc
            i += 1

    print("finished pre-train")