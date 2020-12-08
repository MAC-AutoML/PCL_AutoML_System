""" Training augmented model """
import os
import random

import numpy as np
import torch
import torch.nn as nn
from thop import profile

import utils
from config import Depth_AugmentConfig
from models import get_model
from models.depth_resnet import Depth_resnet

try:
    from torch.utils.tensorboard import SummaryWriter
except ModuleNotFoundError:
    from tensorboardX import SummaryWriter


config = Depth_AugmentConfig()

device = torch.device("cuda")

# tensorboard
writer = SummaryWriter(log_dir=os.path.join(config.path, "tb"))
writer.add_text('config', config.as_markdown(), 0)

logger = utils.get_logger(os.path.join(config.path, "logger.log"))
config.print_params(logger.info)


def main():
    logger.info("Logger is set - training start")
    logger.info('torch version is: {0}'.format(torch.__version__))

    # set default gpu device id
    torch.cuda.set_device(config.gpus[0])

    # set seed
    np.random.seed(config.seed)
    torch.manual_seed(config.seed)
    torch.cuda.manual_seed_all(config.seed)
    random.seed(config.seed)

    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.enabled = True

    # get data with meta info
    input_size, input_channels, n_classes, train_data, valid_data = utils.get_data(
        config.dataset, config.data_path, config.cutout_length, validation=True, autoaugment=config.autoaugment)

    criterion = nn.CrossEntropyLoss().to(device)

    model = Depth_resnet(config.channel, config.factor, config.layers, config.expansion, config.drop_out)
    # if config.genotype is not None:
    #     from models.nas_models import AugmentCNN, Genotype
    #     model = AugmentCNN(32, 3, 36, 10, 20, True, eval(
    #         config.genotype), drop_out=config.drop_out)
    # else:
    #     model = get_model(config.model_name)

    # model size and flops
    macs, params = profile(model, inputs=(torch.randn(1, 3, 32, 32), ))
    macs, params = macs / 1000. / 1000., params / 1000. / 1000.
    logger.info("Model size = {:.3f} M".format(params))
    logger.info("FLOPs = {:.3f} M".format(macs))

    model = nn.DataParallel(model, device_ids=config.gpus).to(device)

    # weights optimizer
    optimizer = torch.optim.SGD(model.parameters(), config.lr, momentum=config.momentum,
                                weight_decay=config.weight_decay)

    train_loader = torch.utils.data.DataLoader(train_data,
                                               batch_size=config.batch_size,
                                               shuffle=True,
                                               num_workers=config.workers,
                                               pin_memory=True)
    valid_loader = torch.utils.data.DataLoader(valid_data,
                                               batch_size=config.batch_size,
                                               shuffle=False,
                                               num_workers=config.workers,
                                               pin_memory=True)
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, config.epochs)

    best_top1 = 0.
    # training loop
    for epoch in range(config.epochs):
        drop_prob = config.drop_path_prob * epoch / config.epochs
        model.module.drop_path_prob(drop_prob)

        # training
        train(train_loader, model, optimizer, criterion, epoch)

        # validation
        cur_step = (epoch+1) * len(train_loader)
        top1 = validate(valid_loader, model, criterion, epoch, cur_step)
        lr_scheduler.step()
        # save
        if best_top1 < top1:
            best_top1 = top1
            is_best = True
            logger.info("Current best Prec@1 = {:.4%}".format(best_top1))
        else:
            is_best = False
        utils.save_checkpoint(model, config.path, is_best)

        print("")

    logger.info("Final best Prec@1 = {:.4%}".format(best_top1))


def train(train_loader, model, optimizer, criterion, epoch):
    top1 = utils.AverageMeter()
    top5 = utils.AverageMeter()
    losses = utils.AverageMeter()

    cur_step = epoch*len(train_loader)
    cur_lr = optimizer.param_groups[0]['lr']
    logger.info("Epoch {} LR {}".format(epoch, cur_lr))
    writer.add_scalar('train/lr', cur_lr, cur_step)

    model.train()

    for step, (X, y) in enumerate(train_loader):
        X, y = X.to(device, non_blocking=True), y.to(device, non_blocking=True)
        N = X.size(0)

        optimizer.zero_grad()
        logits, aux_logits = model(X)
        loss = criterion(logits, y)
        if config.aux_weight > 0.:
            loss += config.aux_weight * criterion(aux_logits, y)
        loss.backward()
        # gradient clipping
        nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
        optimizer.step()

        prec1, prec5 = utils.accuracy(logits, y, topk=(1, 5))
        losses.update(loss.item(), N)
        top1.update(prec1.item(), N)
        top5.update(prec5.item(), N)

        if step % config.print_freq == 0 or step == len(train_loader)-1:
            logger.info(
                "Train: [{:3d}/{}] Step {:03d}/{:03d} Loss {losses.avg:.3f} "
                "Prec@(1,5) ({top1.avg:.1%}, {top5.avg:.1%})".format(
                    epoch+1, config.epochs, step, len(train_loader)-1, losses=losses,
                    top1=top1, top5=top5))

        writer.add_scalar('train/loss', loss.item(), cur_step)
        writer.add_scalar('train/top1', prec1.item(), cur_step)
        writer.add_scalar('train/top5', prec5.item(), cur_step)
        cur_step += 1

    logger.info(
        "Train: [{:3d}/{}] Final Prec@1 {:.4%}".format(epoch+1, config.epochs, top1.avg))


def validate(valid_loader, model, criterion, epoch, cur_step):
    top1 = utils.AverageMeter()
    top5 = utils.AverageMeter()
    losses = utils.AverageMeter()

    model.eval()

    with torch.no_grad():
        for step, (X, y) in enumerate(valid_loader):
            X, y = X.to(device, non_blocking=True), y.to(
                device, non_blocking=True)
            N = X.size(0)

            logits, _ = model(X)
            loss = criterion(logits, y)

            prec1, prec5 = utils.accuracy(logits, y, topk=(1, 5))
            losses.update(loss.item(), N)
            top1.update(prec1.item(), N)
            top5.update(prec5.item(), N)

            if step % config.print_freq == 0 or step == len(valid_loader)-1:
                logger.info(
                    "Valid: [{:3d}/{}] Step {:03d}/{:03d} Loss {losses.avg:.3f} "
                    "Prec@(1,5) ({top1.avg:.1%}, {top5.avg:.1%})".format(
                        epoch+1, config.epochs, step, len(valid_loader)-1, losses=losses,
                        top1=top1, top5=top5))

    writer.add_scalar('val/loss', losses.avg, cur_step)
    writer.add_scalar('val/top1', top1.avg, cur_step)
    writer.add_scalar('val/top5', top5.avg, cur_step)

    logger.info(
        "Valid: [{:3d}/{}] Final Prec@1 {:.4%}".format(epoch+1, config.epochs, top1.avg))

    return top1.avg


if __name__ == "__main__":
    main()
