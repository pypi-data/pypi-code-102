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
"""IQA SYSTEM for evaluation a variety of quality assessment index.

  Referenced by: https://github.com/dingkeyan93/IQA-optimization

  - SSIM, MS-SSIM, CW-SSIM,
  - FSIM, VSI, GMSD,
  - NLPD, MAD,
  - VIF,
  - LPIPS, DISTS.

"""
import os
import argparse
import tqdm
import torch
from torch.utils import tensorboard
import tw
from tw import logger
from tw import transform as T

import full_reference_model


class FullReferenceIQA():

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

    # build optim
    if self.Config.task == 'train':
      self.Optim = torch.optim.Adam([{'params': self.Model.parameters(), 'lr': self.Config.train_lr}])
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self.load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def build_model(self):
    """build iqa models
    """
    cfg = self.Config
    device = self.Config.device

    if cfg.model == 'ssim':
      model = full_reference_model.SSIM()
    elif cfg.model == 'ms_ssim':
      model = full_reference_model.MS_SSIM()
    elif cfg.model == 'cw_ssim':
      model = full_reference_model.CW_SSIM()
    elif cfg.model == 'gmsd':
      model = full_reference_model.GMSD()
    elif cfg.model == 'nlpd':
      model = full_reference_model.NLPD()
    elif cfg.model == 'fsim':
      model = full_reference_model.FSIM()
    elif cfg.model == 'vsi':
      model = full_reference_model.VSI()
    elif cfg.model == 'vif':
      model = full_reference_model.VIF()
    elif cfg.model == 'vifs':
      model = full_reference_model.VIFs()
    elif cfg.model == 'mad':
      model = full_reference_model.MAD()
    elif cfg.model == 'lpips':
      model = full_reference_model.LPIPSvgg()
    elif cfg.model == 'dists':
      model = full_reference_model.DISTS()
    elif cfg.model == 'psnr':
      model = full_reference_model.PSNR()
    else:
      raise NotImplementedError(cfg.model)

    model.to(device)
    return model

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

  @staticmethod
  def transform_train(metas):
    """random crop or padding
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.to_tensor(metas, scale=255.0)
    return metas

  @staticmethod
  def transform_val(metas):
    """center crop or padding
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.to_tensor(metas, scale=255.0)
    return metas

  def build_dataset(self, phase):
    """build dataset
    """
    cfg = self.Config

    if phase == tw.phase.train:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_train, tw.phase.train, split=(0, 180), blind_mode=False)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_train, split=list(range(0, 20)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_train, split=list(range(0, 930)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_train, split=list(range(0, 12)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_train, split=list(range(0, 23)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_train, split=list(range(24)), blind_mode=False)  # nopep8

    elif phase == tw.phase.val:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_val, tw.phase.train, split=(180, 200), blind_mode=False)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_val, split=list(range(20, 25)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_val, split=list(range(930, 1162)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_val, split=list(range(12, 15)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_val, split=list(range(23, 29)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_val, split=list(range(24, 30)), blind_mode=False)  # nopep8

    elif phase == tw.phase.test:
      if cfg.dataset == 'PIPAL':
        dataset = tw.datasets.PIPAL("_datasets/quality_assess/PIPAL", self.transform_val, tw.phase.test, split=(180, 200), blind_mode=False)  # nopep8
      elif cfg.dataset == 'TID2013':
        dataset = tw.datasets.TID2013("_datasets/quality_assess/TID2013/mos_with_names.txt", self.transform_val, split=list(range(20, 25)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'KonIQ10k':
        dataset = tw.datasets.KonIQ10k("_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv", self.transform_val, phase=tw.phase.test)  # nopep8
      elif cfg.dataset == 'LIVEC':
        dataset = tw.datasets.LIVEC("_datasets/quality_assess/LIVEC", self.transform_val, split=list(range(930, 1162)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVEMD':
        dataset = tw.datasets.LIVEMD("_datasets/quality_assess/LIVEMD", self.transform_val, split=list(range(12, 15)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'LIVE2005':
        dataset = tw.datasets.LIVE2005("_datasets/quality_assess/LIVE2005", self.transform_val, split=list(range(23, 29)), blind_mode=False)  # nopep8
      elif cfg.dataset == 'CSIQ':
        dataset = tw.datasets.CSIQ("_datasets/quality_assess/CSIQ/csiq.txt", self.transform_val, split=list(range(24, 30)), blind_mode=False)  # nopep8

    else:
      raise NotImplementedError(phase.value)

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
          batch_size=1,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

  def val(self, **kwargs):
    """val (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()
    self.Evaluator.reset()

    # build dataloader
    dataset = self.build_dataset(tw.phase.val)
    loader = self.build_dataloader(dataset, tw.phase.val)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')
    result_path = os.path.join(root, 'prediction.txt')
    result = open(result_path, 'w')

    # start
    with torch.no_grad():

      for samples in tqdm.tqdm(loader):
        total += len(samples)

        # construct inputs
        refs, distorts, labels, ref_paths, distort_paths = [], [], [], [], []
        for sample in samples:
          refs.append(sample[0].bin.to(device))
          distorts.append(sample[1].bin.to(device))
          labels.append(sample[1].label)
          ref_paths.append(sample[0].path)
          distort_paths.append(sample[1].path)

        # to tensor
        refs = torch.stack(refs, dim=0).float().to(device)
        distorts = torch.stack(distorts, dim=0).float().to(device)
        labels = torch.tensor(labels).float().to(device)

        # inference
        preds = self.Model(refs, distorts, as_loss=False)

        # write to file
        if preds.size(0) == 1:
          result.write('{} {} {} {}\n'.format(ref_paths[0], distort_paths[0], labels.item(), preds.item()))
        else:
          for rp, dp, label, pred in zip(ref_paths, distort_paths, labels.squeeze(), preds.squeeze()):
            result.write('{} {} {} {}\n'.format(rp, dp, label.item(), pred.item()))

        # append
        self.Evaluator.append(preds, labels)

    # stat
    result.close()
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)
    tw.logger.val('Result has been saved in {}'.format(result_path))

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'val':
      with torch.no_grad():
        self.val()

    elif cfg.task == 'viz':
      with torch.no_grad():
        self.viz()

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
  parser.add_argument('--log-val', type=int, default=1, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=None, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

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
  parser.add_argument('--input-height', type=int, default=224, help='network input height.')
  parser.add_argument('--input-width', type=int, default=224, help='network input wdith.')

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
  tw.runner.launch(parser, FullReferenceIQA)
