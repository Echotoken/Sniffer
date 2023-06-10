from torch import nn, optim
import torch.nn.functional as F

class CNN_target(nn.Module):
    def __init__(self):
        super(CNN_target, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool3 = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 3 * 3, 625)
        self.fc2 = nn.Linear(625, 10)

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 3 * 3)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x

class FNN_target(nn.Module):
    def __init__(self):
        super(FNN_target, self).__init__()
        self.fc1 = nn.Linear(784, 100)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):                             
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


class RNN_target(nn.Module):
    def __init__(self):
        super(RNN_target, self).__init__()
        self.lstm = nn.RNN(28, 128, 2, nonlinearity='relu', batch_first=True)
        self.classifier = nn.Linear(128, 10)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.classifier(out)
        return out


