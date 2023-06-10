import torch
import numpy as np

class local_predict:
    def __init__(self, target_model, model_type):
        self.target_model=torch.load(target_model)
        self.type = model_type

    def predictor(self, data):
        if isinstance(data,torch.Tensor):
            data = data.detach().numpy()
        dim = data[0].size
        if len(data.shape)>4:
            print("Only supports inputs up to 4 dimensions.")
            
        if self.type =='RNN':
            while len(data.shape)<3:
                data = np.expand_dims(data, axis=1)
            if len(data.shape)>3:
                data = data.reshape(data.shape[0],data.shape[2], -1)
            data = torch.tensor(data,requires_grad=True).float().to('cpu')
            return self.target_model(data).detach().numpy()
        
        elif self.type =='CNN':
            while len(data.shape) < 4:
                data = np.expand_dims(data, axis=1)
            data = torch.tensor(data,requires_grad=True).float().to('cpu')
            return self.target_model(data).detach().numpy()
        
        elif self.type == "FNN":
            data = data.reshape((-1, dim))
            data = torch.tensor(data, requires_grad=True).float().to('cpu')
            return self.target_model(data).detach().numpy()
        
        else :
            if len(data.shape) > 2:
                data = data.reshape((-1, dim))
            return self.target_model.predict_proba(data)
