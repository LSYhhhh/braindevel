import torch
from torch.autograd import Variable
import numpy as np
import random


def to_net_in_output(X):
    return Variable(torch.from_numpy(X), requires_grad=False)


def set_random_seeds(seed, cuda):
    random.seed(seed)
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def convert_to_dense_prediction_model(model):
    stride_so_far = np.array([1, 1])
    for module in model.modules():
        if hasattr(module, 'stride'):
            stride_so_far *= np.array(module.stride)
            module.stride = (1, 1)
        if hasattr(module, 'dilation'):
            assert module.dilation == 1 or (module.dilation == (1,1)), (
                "Dilation should equal 1 before conversion, maybe the model is "
                "already converted?")
            module.dilation = (int(stride_so_far[0]), int(stride_so_far[1]))
