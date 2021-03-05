'''Pre-activation ResNet in PyTorch.

Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Identity Mappings in Deep Residual Networks. arXiv:1603.05027
'''
import torch
import torch.nn as nn
import torch.nn.functional as F

from models.nas_models import AuxiliaryHead, DropPath_


class PreActBlock(nn.Module):
    '''Pre-activation version of the BasicBlock.'''
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(PreActBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(
            in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.drop_path = DropPath_()

        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes,
                          kernel_size=1, stride=stride, bias=False))

    def forward(self, x):
        out = F.relu(self.bn1(x))
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.conv2(F.relu(self.bn2(out)))
        if self.training:
            out = self.drop_path(out)
        out += shortcut
        return out


class PreActBottleneck(nn.Module):
    '''Pre-activation version of the original Bottleneck module.'''
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(PreActBottleneck, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion *
                               planes, kernel_size=1, bias=False)
        self.drop_path = DropPath_()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes,
                          kernel_size=1, stride=stride, bias=False)
            )

    def forward(self, x):
        out = F.relu(self.bn1(x))
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.conv2(F.relu(self.bn2(out)))
        out = self.conv3(F.relu(self.bn3(out)))
        if self.training:
            out = self.drop_path(out)
        out += shortcut
        return out


class PreActResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10):
        super(PreActResNet, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)

        self.aux_head = AuxiliaryHead(8, 256*block.expansion, 10)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512*block.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv1(x)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        if self.training:
            logits_aux = self.aux_head(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out, logits_aux

    def drop_path_prob(self, p):
        """ Set drop path probability """
        for module in self.modules():
            if isinstance(module, DropPath_):
                module.p = p


class Res_Cell(nn.Module):
    def __init__(self, init_channels, multi_factor, layers, block, num_classes=10):
        super(Res_Cell, self).__init__()
        self._auxiliary = True
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
            self.layers.append(block(self.in_planes, channel, stride))
            self.in_planes = channel * block.expansion
            if i == 2*layers//3:
                self.aux_head = AuxiliaryHead(8, self.in_planes, 10)
        self.layers = nn.Sequential(*self.layers)
        self.linear = nn.Linear(self.in_planes, num_classes)

    def forward(self, x):
        logits_aux = None
        out = F.relu(self.bn1(self.conv1(x)))
        for i, layer in enumerate(self.layers):
            out = layer(out)
            if self.training and i == 2*len(self.layers)//3:
                logits_aux = self.aux_head(out)
        out = F.avg_pool2d(out, 8)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out, logits_aux

    def drop_path_prob(self, p):
        """ Set drop path probability """
        for module in self.modules():
            if isinstance(module, DropPath_):
                module.p = p


def PreActResNet18():
    return PreActResNet(PreActBlock, [2, 2, 2, 2])


def PreActResNet34():
    return PreActResNet(PreActBlock, [3, 4, 6, 3])


def PreActResNet50():
    return PreActResNet(PreActBottleneck, [3, 4, 6, 3])


def PreActResNet101():
    return PreActResNet(PreActBottleneck, [3, 4, 23, 3])


def PreActResNet152():
    return PreActResNet(PreActBottleneck, [3, 8, 36, 3])


def PreBasic_res_cell_64_2_20():
    return Res_Cell(64, 2, 20, PreActBlock)


def PreBottleNeck_res_cell_64_2_20():
    return Res_Cell(64, 2, 20, PreActBottleneck)


def PreBasic_rescell_36_3_20():
    return Res_Cell(36, 3, 20, PreActBlock)


def PreBottleNeck_rescell_36_3_20():
    return Res_Cell(36, 3, 20, PreActBottleneck)


def test():

    print('PreBasic_res_cell_64_2_20 testing:')
    net = PreBasic_res_cell_64_2_20()
    logit, logit_aux = net(torch.randn(2, 3, 32, 32))
    print(logit.size())
    print(logit_aux.size())
    print('pass!')

    print('PreBasic_rescell_36_3_20 testing:')
    net = PreBasic_rescell_36_3_20()
    logit, logit_aux = net(torch.randn(2, 3, 32, 32))
    print(logit.size())
    print(logit_aux.size())
    print('pass!')

    print('PreBottleNeck_res_cell_64_2_20 testing:')
    net = PreBottleNeck_res_cell_64_2_20()
    logit, logit_aux = net(torch.randn(2, 3, 32, 32))
    print(logit.size())
    print(logit_aux.size())
    print('pass!')

    print('PreBottleNeck_rescell_36_3_20 testing:')
    net = PreBottleNeck_rescell_36_3_20()
    logit, logit_aux = net(torch.randn(2, 3, 32, 32))
    print(logit.size())
    print(logit_aux.size())
    print('pass!')

# test()
