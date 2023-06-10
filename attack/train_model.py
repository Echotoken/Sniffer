import torch
import torchvision
from torchvision import transforms
from NN_models import FNN_target, CNN_target, RNN_target
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from local_predictor import local_predict

read = True

if not read:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    batch_size = 64

    train_dataset = torchvision.datasets.MNIST("./dataset/mnist", train=True, transform=transforms.Compose(
        [transforms.ToTensor()]), download=True)
    test_dataset = torchvision.datasets.MNIST("./dataset/mnist", train=False, transform=transforms.Compose(
        [transforms.ToTensor()]), download=True)

    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                            batch_size=batch_size,
                                            shuffle=True)

    test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                            batch_size=batch_size,
                                            shuffle=False)

    model = CNN_target().to(device)


    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    for epoch in range(30):
        model.train()

        for data in train_loader:
            sample, label = data
            sample = sample.squeeze(1)
            # sample = sample.view(-1, 28, 28)
            sample = sample.view(-1, 784)
            sample = sample.to(device)
            label = label.to(device)

            optimizer.zero_grad()
            out = model(sample)
            loss = criterion(out, label)
            loss.backward()
            optimizer.step()

        if epoch % 3 == 0:
            model.eval()

            test_loss = 0
            test_acc = 0  # total sum of right prediction
            total = 0
            for data in test_loader:
                sample, label = data
                sample = sample.squeeze(1)
                # sample = sample.view(-1, 28, 28)
                sample = sample.view(-1, 784)
                sample = sample.to(device)
                label = label.to(device)
                

                with torch.no_grad():
                    out = model(sample)

                loss = criterion(out, label)
                _, pred = torch.max(out, dim=1)
                num_correct = (pred == label).sum()
                test_acc += num_correct.item()
                test_loss += loss.item()
                total += label.size(0)

            print('epoch: {}, loss: {:.4}, accu_rate:{}, total:{}'.format(epoch, test_loss / total, test_acc / total, total))

            torch.save(model, f"epoch_{epoch}_acc{test_acc}.pkl")
else:
    Predictor = local_predict("upload/CNN_MNIST.pkl", "LR")
    print(Predictor.target_model)