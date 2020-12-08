'''ResNet in PyTorch.

For Pre-activation ResNet, see 'preact_resnet.py'.

Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
'''
import torch
import torch.nn as nn
import torch.nn.functional as F

from models.nas_models import AuxiliaryHead, DropPath_


class Bottleneck(nn.Module):
    def __init__(self, in_planes, planes, expansion=4, stride=1):
        super(Bottleneck, self).__init__()
        self.expansion = expansion
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, groups=planes,
                               stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion *
                               planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        self.drop_path = DropPath_()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        if self.training:
            out = self.drop_path(out)
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Res_Cell(nn.Module):
    def __init__(self, init_channels, multi_factor, layers, block, num_classes=10, expansion=4, drop_out=0):
        super(Res_Cell, self).__init__()
        self._dropout = drop_out
        self._auxiliary = True
        self.expansion = expansion
        channel = init_channels
        self.conv1 = nn.Conv2d(3, channel, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channel)
        self.layers = []
        self._multiply_factor = multi_factor
        self.in_planes = channel
        for i in range(layers):
            if i in [layers//3, 2*layers//3]:
                channel *= self._multiply_factor
                stride = 2
            else:
                stride = 1
            self.layers.append(block(self.in_planes, channel,
                                     expansion=self.expansion, stride=stride))
            self.in_planes = channel * self.expansion
            if i == 2*layers//3:
                self.aux_head = AuxiliaryHead(8, self.in_planes, 10)
        self.layers = nn.Sequential(*self.layers)
        self.gap = nn.AdaptiveAvgPool2d(1)
        if self._dropout > 0:
            self.dropout = nn.Dropout(p=self._dropout)
        self.linear = nn.Linear(self.in_planes, num_classes)

    def forward(self, x):
        logits_aux = None
        out = F.relu(self.bn1(self.conv1(x)))
        for i, layer in enumerate(self.layers):
            out = layer(out)
            if self.training and i == 2*len(self.layers)//3:
                logits_aux = self.aux_head(out)
        out = F.gap(out)
        if self._dropout > 0:
            out = self.dropout(out)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out, logits_aux

    def drop_path_prob(self, p):
        """ Set drop path probability """
        for module in self.modules():
            if isinstance(module, DropPath_):
                module.p = p


def BottleNeck_res_cell_64_2_20_4():
    return Res_Cell(64, 2, 20, Bottleneck, expansion=4)


def BottleNeck_rescell_36_3_20_4():
    return Res_Cell(36, 3, 20, Bottleneck, expansion=4)


def Depth_resnet(channel, multi_factor, layer, expansion):
    return Res_Cell(channel, multi_factor, layer, Bottleneck, expansion=expansion)
# def test():

#     print('BottleNeck_res_cell testing:')
#     net = BottleNeck_res_cell_64_2_20_4()
#     logit, logit_aux = net(torch.randn(2, 3, 32, 32))
#     print(logit.size())
#     print(logit_aux.size())
#     print('pass!')


# test()
