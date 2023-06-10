import random
import NNs.Utils as util
import numpy as np
import torch



class sinifsgm:
    def __init__(self, model, device, max_epsilon):
        self.model = model
        self.device = device

        self.max_epsilon = max_epsilon

        self.num_iter = 10

        self.momentum = 1.0

        self.prob = 0.5


    def graph(self, x, y, i, x_max, x_min, grad):

        eps = 2.0 * self.max_epsilon / 255.0
        num_iter = self.num_iter
        alpha = eps / num_iter
        momentum = self.momentum
        x_nes = x + momentum * alpha * grad
        if not isinstance(y,torch.Tensor):
            y = torch.tensor(y).long().to(self.device)
        else:
            y= y.float().clone().detach().requires_grad_(True).long().to(self.device)
        logits_v3 = self.model(x_nes.float())
        pred = np.argmax(logits_v3.detach().numpy(), 1)
        if i == 0:
            first_round = 1
        else:
            first_round = 0
        y = first_round * pred[0] + (1 - first_round) * y
        cross_entropy = torch.nn.functional.cross_entropy(logits_v3, y)
        noise = torch.autograd.grad(cross_entropy, x)[0]
        x_nes_2 = 1 / 2 * x_nes
        logits_v3_2 = self.model(x_nes_2.float())
        cross_entropy_2 = torch.nn.functional.cross_entropy(logits_v3_2, y)
        noise += torch.autograd.grad(cross_entropy_2, x)[0]

        x_nes_4 = 1 / 4 * x_nes
        logits_v3_4 = self.model(x_nes_4.float())

        cross_entropy_4 = torch.nn.functional.cross_entropy(logits_v3_4, y)
        noise += torch.autograd.grad(cross_entropy_4, x)[0]

        x_nes_8 = 1 / 8 * x_nes
        logits_v3_8 = self.model(x_nes_8.float())

        cross_entropy_8 = torch.nn.functional.cross_entropy(logits_v3_8, y)
        noise += torch.autograd.grad(cross_entropy_8, x)[0]

        x_nes_16 = 1 / 16 * x_nes
        logits_v3_16 = self.model(x_nes_16.float())

        cross_entropy_16 = torch.nn.functional.cross_entropy(logits_v3_16, y)
        noise += torch.autograd.grad(cross_entropy_16, x)[0]
        tuple = (0,)
        for j in range(len(noise.detach().numpy().shape)) :
            tuple+=(j,)
        tuple = tuple[2:]
        mean = torch.mean(torch.abs(noise),tuple , True)#

        noise = noise / mean
        noise = momentum * grad + noise
        x = x + alpha * torch.sign(noise)
        x_f = self.clip_by_tensor(x, x_min, x_max)
        i = i + 1
        return x_f, y, i, x_max, x_min, noise

    def clip_by_tensor(self, t, t_min, t_max):
        t = t.float()
        t_min = t_min.float()
        t_max = t_max.float()

        result = (t >= t_min).float() * t + (t < t_min).float() * t_min
        result = (result <= t_max).float() * result + (result > t_max).float() * t_max
        return result

    def attack(self, data, model, adv_number):
        shape = np.expand_dims(data.data[0].detach().numpy(), axis=0).shape

        adver_data = torch.ones(shape).to(self.device)
        adver_label = []
        k = 0
        all_orig_img, all_target_labels, all_orig_labels, all_orig_img_id = util.generate_attack_data_set(data, model)
        success = 0
        while k < adv_number:
            j =random.randint(0, all_orig_img_id.size - 1)
            img = all_orig_img[j:j + 1, ...]
            true = all_orig_labels[j:j + 1]
            true_class = true
            eps = 2.0 * self.max_epsilon / 255.0
            y = [0]
            i = 0
            grad = torch.zeros(shape).to(self.device)
            if len(img.shape) == 3:
                img = np.expand_dims(img, axis=0)
            adv_img = torch.tensor(img,requires_grad=True).to(self.device)

            x_max = torch.clamp(adv_img + eps, -1.0, 1.0)
            x_min = torch.clamp(adv_img - eps, -1.0, 1.0)
            while i < self.num_iter:
                adv_img, y, i, x_max, x_min, grad = self.graph(adv_img, y, i, x_max, x_min, grad)

            if len(adv_img.shape) != len(img.shape):
                adv_img = adv_img.reshape(img.shape)
            adv_out = model(adv_img)

            if isinstance(adv_out,torch.Tensor):
                adv_class = np.argmax(adv_out.detach().numpy(),1)
            else:
                adv_class = np.argmax(adv_out,1)

            if adv_class != true_class:
                success = success + 1
                adv_img = adv_img.squeeze(0)
                adver_data = torch.cat((adver_data, adv_img), 0)
                adver_label.append(true_class)

            k += 1

        if adver_data.shape[0] == 1:
            adver_data = torch.cat((adver_data, adv_img), 0)
            adver_label.append(true_class)

        adver_data = adver_data[1:]
        adver_label = np.array(adver_label)

        return adver_data, adver_label

    def generation(self, img, lab, model):
        eps = 2.0 * self.max_epsilon / 255.0
        y = [0]
        i = 0
        if len(img.shape) == 3:
            shape = np.expand_dims(img,axis=0).shape
        else:
            shape=img.shape
        grad = torch.zeros(shape).to(self.device)
        adv_img = torch.tensor(img,requires_grad=True).float().to(self.device)
        x_max = torch.clamp(adv_img + eps, -1.0, 1.0)
        x_min = torch.clamp(adv_img - eps, -1.0, 1.0)
        while i < 5:
            adv_img, y, i, x_max, x_min, grad = self.graph(adv_img, y, i, x_max, x_min, grad)
        if len(adv_img.shape) != len(img.shape) :
            adv_img = adv_img.reshape(img.shape)
        return adv_img
