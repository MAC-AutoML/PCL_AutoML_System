import timm
import torch
import argparse
import pathlib
import time
try:
    import apex
except ImportError:
    pass
import numpy as np
import torch
import torch.nn as nn
import torch.distributed as dist
import torchvision

from fvcore.common.checkpoint import Checkpointer

from pytorch_image_classification import (
    apply_data_parallel_wrapper,
    create_dataloader,
    create_loss,
    create_model,
    create_optimizer,
    create_scheduler,
    get_default_config,
    update_config,
)
from pytorch_image_classification.config.config_node import ConfigNode
from pytorch_image_classification.utils import (
    AverageMeter,
    DummyWriter,
    compute_accuracy,
    count_op,
    create_logger,
    create_tensorboard_writer,
    find_config_diff,
    get_env_info,
    get_rank,
    save_config,
    set_seed,
    setup_cudnn,
)

def load_config(dconfig = "configs/cifar/resnet56.yaml"):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default=dconfig)
    parser.add_argument('--resume', type=str, default='')
    parser.add_argument('--local_rank', type=int, default=0)
    parser.add_argument('options', default=None, nargs=argparse.REMAINDER)
    args = parser.parse_args()

    config = get_default_config()
    if args.config is not None:
        config.merge_from_file(args.config)
    config.merge_from_list(args.options)
    if not torch.cuda.is_available():
        config.device = 'cpu'
        config.train.dataloader.pin_memory = False
    if args.resume != '':
        config_path = pathlib.Path(args.resume) / 'config.yaml'
        config.merge_from_file(config_path.as_posix())
        config.merge_from_list(['train.resume', True])
    config.merge_from_list(['train.dist.local_rank', args.local_rank])
    config = update_config(config)
    #config.freeze()
    return config
'''
m = timm.create_model('mobilenetv3_large_100', pretrained=True)
m.eval()
torch.save(m, './model.pkl')
model = torch.load('./model.pkl')
model.eval()
print(model)'''
import cus_train
params = {
    "epochs":180,
    "base_lr":0.11,
    "momentum":0.99,
    "weight_decay": 1e-4,
    "lr_decay": 0.11,
}
acc = cus_train.main("resnet56","cifar10",params)
'''
model = "resnet56"
dataset = "cifar10"
config = load_config("configs/cifar/"+str(model)+".yaml")
config.train.output_dir +=str(time.time())
config.scheduler.epochs = params["epochs"]
config.dataset.name = str(dataset).upper()
config.scheduler.lr_decay = params["lr_decay"]
config.train.base_lr = params["base_lr"]
config.train.momentum = params["momentum"]
config.train.weight_decay = params["weight_decay"]


print("########################################")
print(config.dataset.name,config.scheduler.epochs,config.scheduler.lr_decay,config.train.base_lr)
print("########################################")'''