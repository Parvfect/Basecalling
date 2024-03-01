

from torch import nn
import numpy as np


class CNNLayerNorm(nn.Module):
    """Layer normalization built for cnns input"""

    def __init__(self, n_features):
        super(CNNLayerNorm, self).__init__()
        self.layer_norm = nn.LayerNorm(n_features)

    def forward(self, x):
        # x (batch, channel, feature, time)
        return (self.layer_norm(x.transpose(2, 3).contiguous())).transpose(2,3).contiguous()
    

