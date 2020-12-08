import timm
import torch
import argparse
import os
def compute_flops(m,name):
    from thop import clever_format
    from thop import profile
    model = m
    input = torch.randn(1, 3, 224, 224)
    flops, params = profile(model,inputs=(input, ))
    #print(flops, params)
    flops, params = clever_format([flops,params])
    print(name,flops, params) #resnet110 12.508G 1.731M
m = timm.create_model('efficientnet_b3a', pretrained=True)
m.eval()
compute_flops(m,'efficientnet_b3a')

m = timm.create_model('regnetx_032', pretrained=True)
m.eval()
compute_flops(m,'regnetx_032')

m = timm.create_model('skresnext50_32x4d', pretrained=True)
m.eval()
compute_flops(m,'skresnext50_32x4d')

m = timm.create_model('mobilenetv2_120d', pretrained=True)
m.eval()
compute_flops(m,'mobilenetv2_120d')

m = timm.create_model('resnet26', pretrained=True)
m.eval()
compute_flops(m,'resnet26')

m = timm.create_model('mobilenetv2_100', pretrained=True)
m.eval()
compute_flops(m,'mobilenetv2_100')


"""
algorithm\classification\pytorch_automodel\image_classification
精度排序
*efficientnet_b3a 990.31M 12.23M
regnetx_032 3.18G 15.26M
skresnext50_32x4d 4.47G 27.43M
resnet50d 4.36G 25.58M
*mobilenetv2_120d 694.13M 5.83M

resnet26d 2.60G 16.01M
*efficientnet_lite0 400.01M 4.65M
*mobilenetv2_100 315.47M 3.50M
*mobilenetv3_large_100 226.72M 5.48M
"""