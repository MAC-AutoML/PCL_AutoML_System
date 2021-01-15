import timm
import torch
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('--outputdir', type=str, default='./output')
parser.add_argument('--algname', type=str, default='mobilenetv3_large_100')
parser.add_argument('--dataset', type=str, default='imagenet')
args = parser.parse_args()

if not os.path.exists(args.outputdir):
    os.mkdir(args.outputdir)
m = timm.create_model(args.algname, pretrained=True)
m.eval()
torch.save(m,args.outputdir+"/"+args.algname+"_"+args.dataset+".pkl")
from pprint import pprint
model_names = timm.list_models(pretrained=True)
pprint(model_names)