from torch import nn, optim
import torch.nn.functional as F

class FNN1(nn.Module):
    def __init__(self, input, output):
        super().__init__()

        self.fc1 = nn.Linear(input, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, output)

    def forward(self, x):
        x = x.view(x.shape[0], -1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.log_softmax(self.fc3(x), dim=1)
        return x


class FNN2(nn.Module):
    def __init__(self,input,output):
        super().__init__()

        self.fc1 = nn.Linear(input, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, output)

    def forward(self, x):
        x = x.view(x.shape[0], -1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.log_softmax(self.fc4(x), dim=1)
        return x
    

class FNN3(nn.Module):
    def __init__(self, input, output):
        super().__init__()

        self.fc1 = nn.Linear(input, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, output)

    def forward(self, x):
        x = x.view(x.shape[0], -1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))

        x = F.log_softmax(self.fc5(x), dim=1)

        return x


class GRU(nn.Module):
    def __init__(self,input,output):
        super(GRU, self).__init__()
        self.input = input
        self.lstm = nn.GRU(input, 128, 2,batch_first=True)
        self.classifier = nn.Linear(128, output)

    def forward(self, x):
        x = x.reshape(x.shape[0], -1, self.input)
        out, _ = self.lstm(x)
        out = F.relu(out)[:, -1, :]
        out = self.classifier(out)
        return out


class RNN(nn.Module):
    def __init__(self, input, output):
        super(RNN, self).__init__()
        self.input = input
        self.lstm = nn.RNN(input, 128, 2,nonlinearity='relu',batch_first=True)
        self.classifier = nn.Linear(128, output)

    def forward(self, x):
        x = x.reshape(x.shape[0], -1, self.input)
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.classifier(out)
        return out


class lSTM(nn.Module):
    def __init__(self,input ,output):
        super(lSTM, self).__init__()
        self.input = input
        self.lstm = nn.LSTM(input, 128, 2,batch_first=True)
        self.classifier = nn.Linear(128, output)

    def forward(self, x):
        x = x.reshape(x.shape[0], -1, self.input)
        out, _ = self.lstm(x)
        out = F.relu(out)[:, -1, :]
        out = self.classifier(out)
        return out