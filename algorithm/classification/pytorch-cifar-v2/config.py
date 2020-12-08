""" Config class for search/augment """
import argparse
import os
from functools import partial
import torch
import time


def get_parser(name):
    """ make default formatted parser """
    parser = argparse.ArgumentParser(
        name, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # print default value always
    parser.add_argument = partial(parser.add_argument, help=' ')
    return parser


def parse_gpus(gpus):
    if gpus == 'all':
        return list(range(torch.cuda.device_count()))
    else:
        return [int(s) for s in gpus.split(',')]


class BaseConfig(argparse.Namespace):
    def print_params(self, prtf=print):
        prtf("")
        prtf("Parameters:")
        for attr, value in sorted(vars(self).items()):
            prtf("{}={}".format(attr.upper(), value))
        prtf("")

    def as_markdown(self):
        """ Return configs as markdown format """
        text = "|name|value|  \n|-|-|  \n"
        for attr, value in sorted(vars(self).items()):
            text += "|{}|{}|  \n".format(attr, value)

        return text


class AugmentConfig(BaseConfig):
    def build_parser(self):
        parser = get_parser("Augment config")
        parser.add_argument('--model_name', default='nasnet')
        parser.add_argument('--dataset', default='CIFAR10',
                            help='CIFAR10 / MNIST / FashionMNIST')
        parser.add_argument('--batch_size', type=int,
                            default=96, help='batch size')
        parser.add_argument('--lr', type=float,
                            default=0.025, help='lr for weights')
        parser.add_argument('--momentum', type=float,
                            default=0.9, help='momentum')
        parser.add_argument('--weight_decay', type=float,
                            default=3e-4, help='weight decay')
        parser.add_argument('--grad_clip', type=float, default=5.,
                            help='gradient clipping for weights')
        parser.add_argument('--print_freq', type=int,
                            default=200, help='print frequency')
        parser.add_argument('--gpus', default='0', help='gpu device ids separated by comma. '
                            '`all` indicates use all gpus.')
        parser.add_argument('--epochs', type=int, default=600,
                            help='# of training epochs')
        parser.add_argument('--init_channels', type=int, default=36)
        parser.add_argument('--layers', type=int,
                            default=20, help='# of layers')
        parser.add_argument('--seed', type=int, default=2, help='random seed')
        parser.add_argument('--workers', type=int,
                            default=4, help='# of workers')
        parser.add_argument('--aux_weight', type=float,
                            default=0.4, help='auxiliary loss weight')
        parser.add_argument('--cutout_length', type=int,
                            default=16, help='cutout length')
        parser.add_argument('--drop_path_prob', type=float,
                            default=0.2, help='drop path prob')
        parser.add_argument('--drop_out', type=float,
                            default=0, help='drop out rate')
        parser.add_argument(
            '--autoaugment', action='store_true', help='use auto augmentation')
        parser.add_argument('--genotype', type=str,
                            default=None, help='genotype of nasnet')
        return parser

    def __init__(self):
        parser = self.build_parser()
        args = parser.parse_args()
        super().__init__(**vars(args))

        self.data_path = '/gdata/cifar10'
        _path = "{}_{}_{}".format(
            self.model_name, time.strftime("%Y%m%d-%H%M%S"), torch.__version__)
        self.path = os.path.join('./experiments', _path)
        self.gpus = parse_gpus(self.gpus)


class Depth_AugmentConfig(BaseConfig):
    def build_parser(self):
        parser = get_parser("Augment config")
        parser.add_argument('--model_name', default='depth_resnet')
        # 需要调整的结构
        parser.add_argument('--channel', type=int, default=32,
                            help='channel')  # 第一层输入的层数 [8, 64, 8]
        parser.add_argument('--layers', type=int,
                            default=20, help='# of layers')  # 总共的 神经网络层数 [10, 160, 1]
        parser.add_argument('--factor', type=int,
                            default=2, help='# channel multi factor')  # 经过一次 stride=2之后的 翻倍因子 [1, 4, 0.5]
        parser.add_argument('--expansion', type=float,
                            default=1.0, help='# channel expansion')  # 每一个 block之间传递的channel size [0.5, 4]
        #################

        # 需要调整的 训练超参数
        parser.add_argument('--epochs', type=int, default=600,
                            help='# of training epochs')  # 训练的epoch [150, 300, 600, 1200, 1800, 2400]
        parser.add_argument('--aux_weight', type=float,
                            default=0.4, help='auxiliary loss weight')  # 辅助loss权重 [0, 0.9, 0.1]
        parser.add_argument('--cutout_length', type=int,
                            default=16, help='cutout length')  # cutout [0, 24, 4]
        parser.add_argument('--drop_path_prob', type=float,
                            default=0.2, help='drop path prob')  # drop_path_prob [0, 0.9, 0.1]
        parser.add_argument('--drop_out', type=float,
                            default=0, help='drop out rate')  # drop_out [0, 0.9, 0.1]
        #################

        parser.add_argument('--dataset', default='CIFAR10',
                            help='CIFAR10 / MNIST / FashionMNIST')
        parser.add_argument('--batch_size', type=int,
                            default=96, help='batch size')
        parser.add_argument('--lr', type=float,
                            default=0.025, help='lr for weights')
        parser.add_argument('--momentum', type=float,
                            default=0.9, help='momentum')
        parser.add_argument('--weight_decay', type=float,
                            default=3e-4, help='weight decay')
        parser.add_argument('--grad_clip', type=float, default=5.,
                            help='gradient clipping for weights')
        parser.add_argument('--print_freq', type=int,
                            default=200, help='print frequency')
        parser.add_argument('--gpus', default='0', help='gpu device ids separated by comma. '
                            '`all` indicates use all gpus.')

        parser.add_argument('--seed', type=int, default=2, help='random seed')
        parser.add_argument('--workers', type=int,
                            default=4, help='# of workers')
        parser.add_argument(
            '--autoaugment', action='store_true', help='use auto augmentation')
        parser.add_argument('--genotype', type=str,
                            default=None, help='genotype of nasnet')
        return parser

    def __init__(self):
        parser = self.build_parser()
        args = parser.parse_args()
        super().__init__(**vars(args))

        self.data_path = '/gdata/cifar10'
        _path = "{}_{}_{}_{}_{}_{}_{}".format(
            self.model_name, self.channel, self.layers, self.factor, self.expansion, time.strftime("%Y%m%d-%H%M%S"), torch.__version__)
        self.path = os.path.join('./experiments/depth', _path)
        self.gpus = parse_gpus(self.gpus)
