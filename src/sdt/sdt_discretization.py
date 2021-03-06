# -*- coding: utf-8 -*-
""" Discretize the (soft) differentiable tree into normal decision tree according to DDT paper"""
import torch
import torch.nn as nn
import sys
import numpy as np
import copy

def discretize_sdt(original_tree):
    tree = copy.copy(original_tree)
    for name, parameter in tree.named_parameters():
        if name == 'beta':
            setattr(tree, name, nn.Parameter(100*torch.ones(parameter.shape)))

        elif name == 'linear.weight':
            parameters=[]
            for weights in parameter:
                bias = weights[0]
                max_id = np.argmax(np.abs(weights[1:].detach().cpu().numpy()))+1
                max_v = weights[max_id].detach().cpu().numpy()
                new_weights = torch.zeros(weights.shape)
                if max_v>0:
                    new_weights[max_id] = torch.tensor(1)
                else:
                    new_weights[max_id] = torch.tensor(-1)
                new_weights[0] = bias/np.abs(max_v)
                parameters.append(new_weights)
            tree.linear.weight = nn.Parameter(torch.stack(parameters))
    return tree
