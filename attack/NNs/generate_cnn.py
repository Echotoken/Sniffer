from NNs.NN_models import lSTM, RNN, GRU, FNN1, FNN2, FNN3

import torch
import torch.nn as nn
from torchvision import transforms

cfg_m_2 = {
    'CNN1': [64, 'M', 128, 'M'],
    'CNN2': [64, 64, 'M', 128, 128, 'M'],
    'CNN3': [64, 128, 'M', 256, 512, 128, 'M'],
    'FC': [512 * 7 * 7, 4096, 10]
}


class FlattenLayer(torch.nn.Module):
    def __init__(self):
        super(FlattenLayer, self).__init__()

    def forward(self, x):
        return x.view(x.shape[0], -1)


class cnn_m_2(nn.Module):
    def __init__(self, vgg_name, input, fin, output):
        super(cnn_m_2, self).__init__()
        self.input = input
        self.output = output
        self.VGG_layer = self.vgg_block(cfg_m_2[vgg_name])
        self.FC_layer = self.fc_block(fin)

    def forward(self, x):
        if len(x.size()) == 3:
            x = torch.unsqueeze(x, 1)
        out_vgg = self.VGG_layer(x)
        out = out_vgg.view(out_vgg.size(0), -1)
        out = self.FC_layer(out)

        return out

    def vgg_block(self, cfg_vgg):
        layers = []
        in_channels = self.input
        for out_channels in cfg_vgg:
            if out_channels == 'M':
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            else:
                layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False))
                layers.append(nn.ReLU(inplace=True))
                in_channels = out_channels
        return nn.Sequential(*layers)

    def fc_block(self, fin):
        fc_net = nn.Sequential()
        fc_net.add_module("fc", nn.Sequential(
            FlattenLayer(),
            nn.Linear(fin, self.output)
        ))
        return fc_net


class cov1_m_2(nn.Module):
    def __init__(self, vgg_name, input, fin, output):
        super(cov1_m_2, self).__init__()
        self.input = input
        self.output = output
        self.VGG_layer = self.vgg_block(cfg_m_2[vgg_name])
        self.FC_layer = self.fc_block(fin)

    def forward(self, x):
        if len(x.size()) == 2:
            x = torch.unsqueeze(x, 1)
        if x.shape[2] < 4:
            x = x.permute(0, 2, 1)
        out_vgg = self.VGG_layer(x)
        out = out_vgg.view(out_vgg.size(0), -1)
        out = self.FC_layer(out)

        return out

    def vgg_block(self, cfg_vgg):
        layers = []
        in_channels = self.input
        for out_channels in cfg_vgg:
            if out_channels == 'M':
                layers.append(nn.MaxPool1d(kernel_size=2, stride=2))
            else:
                layers.append(nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1, bias=False))
                layers.append(nn.ReLU(inplace=True))
                in_channels = out_channels
        return nn.Sequential(*layers)

    def fc_block(self, fin):
        fc_net = nn.Sequential()
        fc_net.add_module("fc", nn.Sequential(
            FlattenLayer(),
            nn.Linear(fin, self.output)
        ))
        return fc_net


def generate_nn(shape, out):
    if isinstance(shape, int):
        dim = shape
        shape = (1,) + (shape,)
    if len(shape) == 1:
        dim = shape[0]
        shape = (1,) + shape
    else:
        dim = 1
        for i in shape:
            dim *= i
    r_input = 0
    cnn1 = None
    cnn2 = None
    cnn3 = None
    if len(shape) == 2:
        r_input = shape[0]
        if shape[0] >= 4 and shape[1] >= 4:
            cnn1, cnn2, cnn3 = generate_conv2((1,) + shape, out)
        else:
            cnn1, cnn2, cnn3 = generate_conv1(shape, out)
    elif len(shape) == 3:
        r_input = shape[0] * shape[1]
        cnn1, cnn2, cnn3 = generate_conv2(shape, out)
    fnn1 = FNN1(dim, out)
    fnn2 = FNN2(dim, out)
    fnn3 = FNN3(dim, out)
    gru = GRU(r_input, out)
    lstm = lSTM(r_input, out)
    rnn = RNN(r_input, out)
    return cnn1, cnn2, cnn3, fnn1, fnn2, fnn3, rnn, lstm, gru


def generate_conv2(shape, out):
    c_input = shape[0]
    f1 = int(((int((shape[1] - 2) / 2) + 1) - 2) / 2) + 1
    f2 = int(((int((shape[2] - 2) / 2) + 1) - 2) / 2) + 1
    f_in = int(128 * f1 * f2)
    return cnn_m_2("CNN1", c_input, f_in, out), cnn_m_2("CNN2", c_input, f_in, out), cnn_m_2("CNN3", c_input, f_in, out)


def generate_conv1(shape, out):
    if shape[1] < 4:
        c_input = shape[1]
        f1 = int((int(((shape[0] - 2) / 2 + 1)) - 2) / 2 + 1)
    else:
        c_input = shape[0]
        f1 = int((int(((shape[1] - 2) / 2 + 1)) - 2) / 2 + 1)
    f_in = int(128 * f1)
    return cov1_m_2("CNN1", c_input, f_in, out), cov1_m_2('CNN2', c_input, f_in, out), cov1_m_2('CNN3', c_input, f_in, out)