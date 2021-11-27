# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Blind IQA System
"""
import os
import argparse
import tqdm
import numpy as np

import torch
from torch import nn
from torch import distributed
from torch.utils import data, tensorboard

import tw
from tw import logger
from tw import transform as T

import models


class BlindIQA():

  def __init__(self, config):
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)
    self.Evaluator = tw.evaluator.QualityAssessEvaluator()

    # scalar
    self.Epoch = 0
    self.Step = 0

    # models
    self.Model = self.build_model()

    # optim
    self.Optim = self.build_optim(self.Model)
    self.Loss = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self.load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def dump(self):
    """dump current checkpoint
    """
    cfg = self.Config
    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'
    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': self.Optim.state_dict(),
    }, path)
    logger.info(f'Model has saved in {path}')

  def load(self):
    """Loading mode
    """
    cfg = self.Config

    logger.net('Loading model source: {}'.format(cfg.model_source))
    ckpt = tw.checkpoint.load(cfg.model_path)

    if cfg.model_source is None:
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    elif cfg.model_source == 'tw':
      content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

      if cfg.task == 'train' and self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    else:
      raise NotImplementedError(cfg.model_source)

  def build_model(self):
    """build iqa models
    """
    cfg = self.Config
    device = self.Config.device

    if cfg.model == 'hyper_iqa':
      model = models.HyperNet(16, 112, 224, 112, 56, 28, 14, 7)

    elif cfg.model.startswith('base'):
      backbone = cfg.model.split('.')[1]
      model = models.BaseIQA(backbone=backbone)

    elif cfg.model.startswith('compose'):
      backbone = cfg.model.split('.')[1]
      model = models.ComposeBlindIQA(backbone=backbone)

    elif cfg.model.startswith('koncept'):
      backbone = cfg.model.split('.')[1]
      model = models.KonCept512(backbone=backbone)

    elif cfg.model.startswith('attributenet'):
      if cfg.dataset == 'SPAQ':
        model = models.AttributeNet('mobilenet_v2', [6, ])

    elif cfg.model.startswith('vqa_v3'):
      model = models.VQAv3(num_classes=1)

    else:
      raise NotImplementedError(cfg.model)

    model.to(device)
    return model

  def build_optim(self, model: nn.Module):
    """build iqa optimizer
    """
    cfg = self.Config
    device = self.Config.device
    task = self.Config.task

    if task == 'train':
      if cfg.model.startswith('koncept'):
        optim = torch.optim.Adam([
            {'params': model.head.parameters(), 'lr': 1e-2},
            {'params': model.cls_head.parameters(), 'lr': 1e-2},
            {'params': model.backbone.parameters(), 'lr': 1e-4}
        ], lr=1e-2, weight_decay=0.0)
      elif cfg.model.startswith('attributenet'):
        optim = torch.optim.Adam([
            {'params': model.attrs.parameters(), 'lr': 1e-3},
            {'params': model.backbone.parameters(), 'lr': 1e-4}
        ], lr=1e-2, weight_decay=0.0)
      else:
        optim = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=0.0)
    else:
      optim = None

    return optim

  @staticmethod
  def transform_train(metas):
    """random crop or padding
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.random_crop_and_pad(metas, target_height=672, target_width=448, fill_value=0)
    T.random_hflip(metas)
    T.to_tensor(metas, scale=255, mean=[0.485, 0.456, 0.406], std=(0.229, 0.224, 0.225))
    return metas

  @staticmethod
  def transform_val(metas):
    """center crop or padding
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.center_crop_and_pad(metas, target_height=672, target_width=448, fill_value=0)
    T.to_tensor(metas, scale=255, mean=[0.485, 0.456, 0.406], std=(0.229, 0.224, 0.225))
    return metas

  def build_dataset(self, phase):
    """build dataset
    """
    cfg = self.Config

    if phase == tw.phase.train:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_train, tw.phase.train, split=(0, 180), blind_mode=True)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_train, split=list(range(0, 20)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'KonIQ10k':
        dataset = tw.datasets.KonIQ10k("_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv", self.transform_train, phase=tw.phase.train)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_train, split=list(range(0, 930)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_train, split=list(range(0, 12)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_train, split=list(range(0, 23)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_train, split=list(range(24)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'FLIVE':
        dataset = tw.datasets.FLIVE("_datasets/quality_assess/FLIVE/all_patches.csv", self.transform_train, phase=tw.phase.train)  # nopep8
      elif cfg.dataset == 'SPAQ':
        dataset = tw.datasets.SPAQ("_datasets/quality_assess/SPAQ", self.transform_train, phase=tw.phase.train)  # nopep8

    elif phase == tw.phase.val:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_val, tw.phase.train, split=(180, 200), blind_mode=True)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_val, split=list(range(20, 25)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'KonIQ10k':
        dataset = tw.datasets.KonIQ10k("_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv", self.transform_val, phase=tw.phase.test)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_val, split=list(range(930, 1162)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_val, split=list(range(12, 15)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_val, split=list(range(23, 29)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_val, split=list(range(24, 30)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'FLIVE':
        dataset = tw.datasets.FLIVE("_datasets/quality_assess/FLIVE/all_patches.csv", self.transform_val, phase=tw.phase.val)  # nopep8
      elif cfg.dataset == 'SPAQ':
        dataset = tw.datasets.SPAQ("_datasets/quality_assess/SPAQ", self.transform_val, phase=tw.phase.val)  # nopep8

    elif phase == tw.phase.test:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_val, tw.phase.test, split=(180, 200), blind_mode=True)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_val, split=list(range(20, 25)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'KonIQ10k':
        dataset = tw.datasets.KonIQ10k("_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv", self.transform_val, phase=tw.phase.test)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_val, split=list(range(930, 1162)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_val, split=list(range(12, 15)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_val, split=list(range(23, 29)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_val, split=list(range(24, 30)), blind_mode=True)  # nopep8
      elif cfg.dataset == 'FLIVE':
        dataset = tw.datasets.FLIVE("_datasets/quality_assess/FLIVE/all_patches.csv", self.transform_val, phase=tw.phase.test)  # nopep8
      elif cfg.dataset == 'SPAQ':
        dataset = tw.datasets.SPAQ("_datasets/quality_assess/SPAQ", self.transform_val, phase=tw.phase.test)  # nopep8

    else:
      raise NotImplementedError(phase.value)

    # scale dataset
    if cfg.dataset == 'PIPAL':
      self.ScaleMax, self.ScaleMin = 1835.99, 934.95
    elif cfg.dataset == 'TID2013':
      self.ScaleMax, self.ScaleMin = 7.21, 0.24
    elif cfg.dataset == 'KonIQ10k':
      self.ScaleMax, self.ScaleMin = 88.39, 3.91
    elif cfg.dataset == 'LIVEC':
      self.ScaleMax, self.ScaleMin = 92.43, 3.42
    elif cfg.dataset == 'LIVEMD':
      self.ScaleMax, self.ScaleMin = 73.65, 17.92
    elif cfg.dataset == 'LIVE2005':
      self.ScaleMax, self.ScaleMin = 111.77, -2.64
    elif cfg.dataset == 'CSIQ':
      self.ScaleMax, self.ScaleMin = 1.00, 0.00
    elif cfg.dataset == 'SPAQ':
      self.ScaleMax, self.ScaleMin = 100.00, 0.00

    return dataset

  def build_dataloader(self, dataset, phase):
    """build dataloader

    Args:
        dataset ([type]): [description]
        phase ([type]): [description]

    Returns:
        [type]: [description]
    """
    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=self.Config.train_batchsize,
          shuffle=True,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=True)

    else:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=4,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

  def optimize(self, samples, **kwargs):
    """forward phase

    Args:
        inputs ([torch.Tensor]): [N, C, H, W]
        labels ([torch.Tensor]): [N, ]

    Returns:
        losses (dict): 
    """
    cfg = self.Config
    device = self.Config.device

    # prepare inputs and targets
    inputs, labels = [], []
    for sample in samples:
      inputs.append(sample[0].bin.to(device, non_blocking=True))
      labels.append(sample[0].label)
    inputs = torch.stack(inputs, dim=0)
    labels = torch.tensor(labels).float().to(device)
    labels = (labels - self.ScaleMin) / (self.ScaleMax - self.ScaleMin)

    # define losses
    if self.Loss is None:
      self.Loss = {
          'l1': tw.nn.losses.L1Loss(),
          'mse': nn.MSELoss(),
          'rank': tw.nn.losses.MonotonicityRelatedLoss(),
          'plcc': tw.nn.losses.PLCCLoss(),
      }

    # define
    losses = {}

    # inference
    if cfg.model == 'hyper_iqa':
      paras = self.Model(inputs)
      model_target = models.TargetNet(paras).to(device)
      for param in model_target.parameters():
        param.requires_grad = False
      preds = model_target(paras['target_in_vec'])
      losses['loss_l1'] = self.Loss['l1'](preds.squeeze(), labels.float())

    elif cfg.model.startswith('base'):
      preds = self.Model(inputs)
      losses['rank'] = self.Loss['rank'](preds, labels)
      losses['loss_l1'] = self.Loss['l1'](preds.squeeze(), labels.float())

    elif cfg.model.startswith('compose'):
      preds = self.Model(inputs)
      losses['loss_mse'] = self.Loss['mse'](preds.squeeze(), labels.float())

    elif cfg.model.startswith('koncept'):
      preds = self.Model(inputs)
      losses['loss_l1'] = self.Loss['l1'](preds.squeeze(), labels.float())

    elif cfg.model.startswith('attributenet'):
      captions = torch.tensor([sample[0].caption for sample in samples]).float().to(device)
      captions = (captions - self.ScaleMin) / (self.ScaleMax - self.ScaleMin)
      preds = self.Model(inputs)
      losses['loss_l1'] = self.Loss['l1'](preds, captions)

    else:
      raise NotImplementedError(cfg.model)

    return losses

  def inference(self, inputs, **kwargs):
    """forward phase

    Args:
        inputs ([torch.Tensor]): [N, C, H, W]

    Returns:
        predictions ([torch.Tensor]): [N, ]
    """
    cfg = self.Config
    device = self.Config.device
    model = self.Model.module if cfg.multiprocess else self.Model

    if cfg.model == 'hyper_iqa':
      paras = model(inputs)
      model_target = models.TargetNet(paras).to(device)
      for param in model_target.parameters():
        param.requires_grad = False
      preds = model_target(paras['target_in_vec'])
      return preds

    elif cfg.model.startswith('base'):
      return model(inputs).squeeze()

    elif cfg.model.startswith('compose'):
      return model(inputs).squeeze()

    elif cfg.model.startswith('koncept'):
      return model(inputs).squeeze()
    
    elif cfg.model.startswith('attributenet'):
      return model(inputs)[:, 0].squeeze()
    
    elif cfg.model.startswith('vqa_v3'):
      return model(inputs).squeeze()

    raise NotImplementedError

  def train(self):
    """training
    """
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_set = self.build_dataset(tw.phase.train)
    train_loader = self.build_dataloader(train_set, tw.phase.train)
    total_step = len(train_loader) * cfg.train_epoch

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # lr scheduler
    lr_sche = torch.optim.lr_scheduler.MultiStepLR(self.Optim, [20, 30, 40], 0.1, -1)

    # training
    while self.Epoch < cfg.train_epoch:
      self.Epoch += 1
      self.Model.train()

      # training a epoch
      for samples in train_loader:
        self.Step += 1

        # inference
        losses = self.optimize(samples)

        # accumulate
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()

        # iter
        losses.update({
            'loss': sum(loss for loss in losses.values()),
            'time': logger.toc(),
        })
        stat.update(losses)
        logger.tic()

        # print
        if tw.runner.reach(self.Step, cfg.log):
          eta = tw.timer.remain_eta(self.Step, total_step, start_time, init_step)
          tw.runner.log(keys=['eta'] + stat.keys() + ['lr'],
                        values=[eta] + stat.values() + [self.Optim.param_groups[0]['lr']],
                        step=self.Step,
                        epoch=self.Epoch,
                        tag='train',
                        iters_per_epoch=len(train_loader),
                        writer=self.Writer)
          stat.reset()

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self.dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        self.val()

      # if tw.runner.reach(self.Epoch, cfg.log_test) and self.Master:
      #   self.test()

      # learning rate scheduler
      lr_sche.step()

  def val(self, loader=None, **kwargs):
    """val (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()

    # reset
    self.Model.eval()
    self.Evaluator.reset()

    # dataset
    if loader is None:
      dataset = self.build_dataset(tw.phase.val)
      loader = self.build_dataloader(dataset, tw.phase.val)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')
    result_path = os.path.join(root, 'prediction.txt')
    result = open(result_path, 'w')

    # start
    with torch.no_grad():
      for samples in tqdm.tqdm(loader):
        # prepare inputs
        inputs, labels, paths = [], [], []
        for sample in samples:
          inputs.append(sample[0].bin.to(device, non_blocking=True))
          labels.append(sample[0].label)
          paths.append(sample[0].path)
        inputs = torch.stack(inputs, dim=0)
        labels = torch.tensor(labels).float().to(device)
        labels = (labels - self.ScaleMin) / (self.ScaleMax - self.ScaleMin)

        # inference
        preds = self.inference(inputs)

        # write to file
        for i, path in enumerate(paths):
          result.write('{} {} {}\n'.format(path, labels[i].item(), preds[i].item()))

        # append
        self.Evaluator.append(preds, labels)

    # stat
    result.close()
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, len(loader))
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)
    tw.logger.val('Result has been saved in {}'.format(result_path))

    return reports

  # def test(self, **kwargs):
  #   """test (ref, distort)"""
  #   cfg = self.Config
  #   device = self.Config.device
  #   start_time = tw.timer.tic()
  #   total = 0

  #   # reset
  #   self.Model.eval()
  #   self.Evaluator.reset()

  #   # build dataloader
  #   if 'loader' in kwargs and kwargs['loader'] is not None:
  #     loader = kwargs['loader']
  #   else:
  #     loader = common.build_dataset(cfg, tw.phase.test, blind_mode=True)

  #   # create folder for every epoch
  #   root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
  #   result_path = os.path.join(root, 'prediction.txt')
  #   result = open(result_path, 'w')

  #   # start
  #   with torch.no_grad():

  #     for images, labels, paths in tqdm.tqdm(loader):

  #       total += images.size(0)

  #       images = images.float().to(device, non_blocking=True)
  #       labels = labels.float().to(device, non_blocking=True)

  #       if images.ndim == 5:
  #         preds = []
  #         for image in images:
  #           pred = self._inference(image)
  #           preds.append(pred.mean())
  #         preds = torch.tensor(preds)
  #       else:
  #         preds = self._inference(images)
  #         if preds.ndim == 0:
  #           preds = preds.reshape([-1])

  #       # write to file
  #       for path, label, pred in zip(paths, labels, preds):
  #         result.write('{} {} {}\n'.format(path, label.item(), pred.item()))

  #       # append
  #       self.Evaluator.append(preds, labels)

  #   # stat
  #   result.close()
  #   reports = self.Evaluator.accumulate()
  #   elapsed = tw.timer.duration(start_time, tw.timer.tic())
  #   throughput = tw.timer.throughput(elapsed, total)
  #   keys = list(reports.keys()) + ['time', 'throughtput']
  #   vals = list(reports.values()) + [elapsed, throughput]
  #   tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)
  #   tw.logger.val('Result has been saved in {}'.format(result_path))

  #   return reports

  def viz(self, **kwargs):
    """inference a mp4/yuv video clip"""
    cfg = self.Config
    device = cfg.device

    # visualize during training
    viz_output = cfg.viz_output if 'viz_output' not in kwargs else kwargs['viz_output']
    viz_input = cfg.viz_input if 'viz_input' not in kwargs else kwargs['viz_input']

    # mkdir
    images, videos = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # to eval
    self.Model.eval()

    # process video
    # for filepath in sorted(videos):
    #   reader = tw.media.VideoReader(filepath, to_rgb=False, to_tensor=False)
    #   results = []
    #   print(filepath)
    #   fw = open(viz_output + '/' + os.path.basename(filepath) + '.txt', 'w')
    #   for i, src in enumerate(reader):
    #     meta = self.transform_val([T.ImageMeta(binary=src)])[0]
    #     images = meta.bin.float().to(device).unsqueeze(dim=0)
    #     preds = self._inference(images)
    #     results.append(preds.cpu().numpy())
    #     fw.write('{}, {}\n'.format(i, list(preds.cpu().numpy())))
    #   fw.close()

    # process images
    fw = open(viz_output + '/' + os.path.basename(viz_input) + '.txt', 'w')
    for filepath in sorted(images):
      meta = self.transform_val([T.ImageMeta(path=filepath).load()])[0]
      images = meta.bin.float().to(device).unsqueeze(dim=0)
      preds = self.inference(images)
      line = '{}, {}\n'.format(filepath, preds.item())
      tw.logger.info(line)
      fw.write(line)
    fw.close()

  def onnx(self, **kwargs):
    """export model to onnx
    """
    cfg = self.Config

    if cfg.model.startswith('vqa_v3'):
      inputs = torch.rand(1, 3, 672, 448).to(cfg.device)
    else:
      raise NotImplementedError(cfg.model)

    tw.flops.register(self.Model)
    self.Model.eval()
    with torch.no_grad():
      self.Model(inputs)
    print(tw.flops.accumulate(self.Model))
    tw.flops.unregister(self.Model)

    tw.export.torch_to_onnx(self.Model.eval(),
                            inputs.to(cfg.device),
                            cfg.model + '.onnx',
                            opset_version=9,
                            input_names=['input', ],
                            output_names=['output', ])

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self.train()

    elif cfg.task == 'val':
      with torch.no_grad():
        self.val()

    elif cfg.task == 'test':
      with torch.no_grad():
        self.test()

    elif cfg.task == 'viz':
      with torch.no_grad():
        self.viz()

    elif cfg.task == 'onnx':
      with torch.no_grad():
        self.onnx()

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset', type=str, default=None)

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=50, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=None, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=50, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model', type=str, default=None, help="IQA evaluator.")
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY INPUT-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--input-colorspace', type=str, default='RGB', choices=['Y', 'RGB', 'YUV'])

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-batchsize', type=int, default=32, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=100, help="total training epochs.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, default='viz.txt', help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  args, _ = parser.parse_known_args()
  tw.runner.launch(parser, BlindIQA)
