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
"""Refactor RandLA-Net in terms of NCHW format.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


#!<-----------------------------------------------------------------------------
#!< Basic Op
#!<-----------------------------------------------------------------------------


def conv1d(in_channels, out_channels, kernel_size, stride, padding, bn=True, activation=True):
  return nn.Sequential(
      nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding, bias=True),
      nn.BatchNorm1d(out_channels) if bn else nn.Identity(),
      nn.LeakyReLU(negative_slope=0.2, inplace=True) if activation else nn.Identity())


def conv2d(in_channels, out_channels, kernel_size, stride, padding, bn=True, activation=True):
  return nn.Sequential(
      nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=True),
      nn.BatchNorm2d(out_channels) if bn else nn.Identity(),
      nn.LeakyReLU(negative_slope=0.2, inplace=True) if activation else nn.Identity())


def gather_neighbour(feature, neighbor_idx):
  """gather point clouds neighbour points

  Args:
      feature ([torch.Tensor]): [bs, ndim, num_points, 1]
      neighbor_idx ([torch.Tensor]): [bs, num_points, num_neighbor]

  Returns:
      [torch.Tensor]: [bs, ndim, num_points, num_neighbor]
  """
  assert feature.ndim == 4 and feature.size(3) == 1, f"require [bs, ndim, num_points, 1] vs {feature.shape}"
  assert neighbor_idx.ndim == 3, f"require input meets [bs, num_points, num_neighbor] vs {neighbor_idx.shape}"
  assert feature.size(2) == neighbor_idx.size(1)
  feature = feature.squeeze(3)

  bs, ndim, num_points = feature.shape
  num_neighbor = neighbor_idx.shape[2]
  index_input = neighbor_idx.reshape(bs, 1, num_points * num_neighbor)
  features = torch.gather(input=feature, dim=2, index=index_input.repeat(1, ndim, 1))
  features = features.reshape(bs, ndim, num_points, num_neighbor)
  return features


def nearest_upsample(feature, interp_idx):
  """point cluster upsample operation.

  Args:
      feature ([torch.Tensor]): [bs, ndim, num_points, 1]
      interp_idx ([torch.Tensor]): [bs, up_num_points, neighbour]

  Note:
      generally, up_num_points = scale * num_points

  Returns:
      [torch.Tensor]: [bs, ndim, up_num_points, 1]
  """
  assert feature.ndim == 4 and feature.size(3) == 1, f"require [bs, ndim, num_points, 1] vs {feature.shape}"
  assert interp_idx.ndim == 3, f"require [bs, up_num_points, neighbour] vs {interp_idx.shape}"

  batch_size, up_num_points = interp_idx.size(0), interp_idx.size(1)
  ndim = feature.size(1)

  # reshape to [bs, up_num_points, 1]
  interp_idx = interp_idx.reshape(batch_size, up_num_points, 1)

  # repeat to [bs, ndim, up_num_points]
  index = interp_idx.unsqueeze(1).repeat(1, ndim, 1, 1)

  # pick up neighbour points: [bs, ndim, up_num_points, 1]
  interpolated_feature = torch.gather(feature, 2, index)

  return interpolated_feature


def nearest_downsample(feature, sub_idx):
  """sample point from feature in terms of sub_idx.

  Args:
      feature ([torch.Tensor]): [bs, ndim, num_points, 1]
      sub_idx ([torch.Tensor]): [bs, sub_num_points, neighbour]

  Note:
      generally, num_points = scale * sub_num_points

  Returns:
      pool_features ([torch.Tensor]): [bs, ndim, sub_num_points, neighbour]
  """
  assert feature.ndim == 4 and feature.size(3) == 1, f"require [bs, ndim, num_points, 1] vs {feature.shape}"
  assert sub_idx.ndim == 3, f"require [bs, sub_num_points, neighbour] vs {sub_idx.shape}"

  bs, ndim = feature.shape[0], feature.shape[1]
  num_neigh = sub_idx.shape[-1]

  # [bs, ndim, num_points]
  feature = feature.squeeze(dim=3)
  # [bs, sub_num_points * num_neighbor]
  sub_idx = sub_idx.reshape(bs, -1)

  # index from [bs, sub_num_points * num_neighbor] to [bs, 1, sub_num_points * num_neighbor]
  # # repeat second dim to [bs, ndim, sub_num_points * num_neighbor]
  index = sub_idx.unsqueeze(1).repeat(1, ndim, 1)

  # pick element according with `index` at dim 2 (num_points)
  pool_features = torch.gather(feature, 2, index)

  # [bs, ndim, num_points -> [bs, ndim, sub_num_points, num_neighbor]
  pool_features = pool_features.reshape(bs, ndim, -1, num_neigh)

  return pool_features


def nearest_max_downsample(feature, sub_idx):
  """sample point from feature in terms of sub_idx with max value.

    It actually does downsample operation among nearest points (e.g. 16) to
      pick up maximum feature value, while the feature maybe varied.

  Args:
      feature ([torch.Tensor]): [bs, ndim, num_points, 1]
      sub_idx ([torch.Tensor]): [bs, sub_num_points, neighbour]

  Note:
      generally, num_points = scale * sub_num_points

  Returns:
      pool_features ([torch.Tensor]): [bs, ndim, sub_num_points, 1]
  """
  pool_features = nearest_downsample(feature, sub_idx)

  # select max neighbour feature -> [16, 32, 4096, 1]
  pool_features = pool_features.max(dim=3, keepdim=True)[0]

  return pool_features


def relative_pos_encoding(xyz, neigh_idx):
  """build relationship between xyz and its neighbours by: (x-x')^2, |x-x'|, x, x'

  Args:
      xyz ([torch.Tensor]): [bs, 3, num_points, 1]
      neigh_idx ([torch.Tensor]): [bs, num_points, num_neighbour]

  Returns:
      [torch.Tensor]: [bs, 10, num_points, num_neighbour]
  """
  assert xyz.ndim == 4 and xyz.size(1) == 3, f"require xyz is [bs, 3, num_points, 1] vs {xyz.shape}"
  assert neigh_idx.ndim == 3, f"require neigh_idx is [bs, num_points, num_neighbour] vs {neigh_idx.shape}"

  # pick current xyz neighbour points [bs, 3, num_points, num_neighbour]
  neighbor_xyz = gather_neighbour(xyz, neigh_idx)

  # repeat to num_neighbour points [bs, 3, num_points, num_neighbour]
  xyz_tile = xyz.repeat(1, 1, 1, neigh_idx.shape[-1])

  # relative distance between xyz and its neighbours
  relative_xyz = xyz_tile - neighbor_xyz

  # euclidean distance (sphere) [bs, 1, num_points, num_neighbor]
  relative_dis = torch.sqrt(torch.sum(torch.pow(relative_xyz, 2), dim=1, keepdim=True))

  # (x-x')^2, |x-x'|, x, x' [bs, 10, num_points, num_neighbour]
  relative_feature = torch.cat([relative_dis, relative_xyz, xyz_tile, neighbor_xyz], dim=1)

  return relative_feature

#!<-----------------------------------------------------------------------------
#!< Module
#!<-----------------------------------------------------------------------------


class AttentionPooling(nn.Module):

  def __init__(self, d_in, d_out):
    super(AttentionPooling, self).__init__()
    self.fc = nn.Conv2d(d_in, d_in, 1, 1, 0, bias=True)
    self.mlp = conv2d(d_in, d_out, 1, 1, 0)

  def forward(self, feature):
    """simple attention with sum pooling: fc((softmax(fc(x)) * x).sum(dim=3))

    Args:
        feature ([torch.Tensor]): [bs, d_in, num_points, num_neighbor]

    Returns:
        [torch.Tensor]: [bs, d_out, num_points, 1]
    """
    att_activation = self.fc(feature)
    att_scores = F.softmax(att_activation, dim=3)
    f_agg = feature * att_scores
    f_agg = torch.sum(f_agg, dim=3, keepdim=True)
    f_agg = self.mlp(f_agg)
    return f_agg


class DilatedResidualBlock(nn.Module):

  def __init__(self, d_out):
    super(DilatedResidualBlock, self).__init__()

    self.mlp1 = conv2d(10, d_out // 2, 1, 1, 0)
    self.att_pooling_1 = AttentionPooling(d_out, d_out // 2)

    self.mlp2 = conv2d(d_out // 2, d_out // 2, 1, 1, 0)
    self.att_pooling_2 = AttentionPooling(d_out, d_out)

  def forward(self, xyz, feature, neigh_idx):
    """(xyz)->LocSE + AttentivePooling + (xyz)->LocSE + Attentive Pooling

    Args:
        xyz ([torch.Tensor]): [bs, 3, num_points, 1]
        feature ([torch.Tensor]): [bs, ndim, num_points, 1]
        neigh_idx ([torch.Tensor]): [bs, num_points, num_neighbour]

    Returns:
        [torch.Tensor]: [bs, 2 * ndim, num_points, 1]
    """

    # [bs, 10, num_points, num_neighbour]
    f_xyz = relative_pos_encoding(xyz, neigh_idx)

    # [bs, ndim, num_points, num_neighbour] xyz mapping to same dim with feature
    f_xyz1 = self.mlp1(f_xyz)

    # [bs, ndim, num_points, num_neighbour]
    f_neighbours = gather_neighbour(feature, neigh_idx)

    # [bs, 2 * ndim, num_points, num_neighbor]
    f_concat = torch.cat([f_neighbours, f_xyz1], dim=1)

    # [bs, ndim, num_points, 1]
    f_pc_agg = self.att_pooling_1(f_concat)

    # ---------

    # [bs, ndim, num_points, num_neighbor]
    f_xyz2 = self.mlp2(f_xyz1)

    # [bs, ndim, num_points, num_neighbor]
    f_neighbours = gather_neighbour(f_pc_agg, neigh_idx)

    # [bs, 2 * ndim, num_points, num_neighbor]
    f_concat = torch.cat([f_neighbours, f_xyz2], dim=1)

    # [bs, 2 * ndim, num_points, 1]
    f_pc_agg = self.att_pooling_2(f_concat)

    return f_pc_agg


class DilatedResidualAttention(nn.Module):

  def __init__(self, d_in, d_out):
    super(DilatedResidualAttention, self).__init__()
    self.mlp1 = conv2d(d_in, d_out // 2, 1, 1, 0)
    self.lfa = DilatedResidualBlock(d_out)
    self.mlp2 = conv2d(d_out, d_out * 2, 1, 1, 0, activation=False)
    self.shortcut = conv2d(d_in, d_out * 2, 1, 1, 0, activation=False)
    self.out = nn.LeakyReLU(negative_slope=0.2, inplace=True)

  def forward(self, feature, xyz, neigh_idx):
    """Dilated Residual Block: (N, din) -> (N, 2*dout)

    Args:
        feature ([torch.Tensor]): [bs, ndim, num_points, 1]
        xyz ([torch.Tensor]): [bs, 3, num_points, 1]
        neigh_idx ([torch.Tensor]): [bs, num_points, num_neighbor]

    Returns:
        [torch.Tensor]: [bs, 2 * ndim_out, num_points, 1]
    """
    f_pc = self.mlp1(feature)
    f_pc = self.lfa(xyz, f_pc, neigh_idx)
    f_pc = self.mlp2(f_pc)
    shortcut = self.shortcut(feature)
    return self.out(f_pc + shortcut)


class RandLANetMultiHead(nn.Module):

  def __init__(self, num_classes=13, num_layers=6, in_channels=8, feature_dims=[16, 64, 128, 256, 512]):
    super(RandLANetMultiHead, self).__init__()
    self.num_layers = num_layers
    self.num_classes = num_classes

    # mapping xyz-rgb to feature space
    self.stem = conv1d(6, in_channels, 1, 1, 0)

    # build encoder blocks
    d_in = in_channels
    self.dilated_res_blocks = nn.ModuleList()
    for index in range(num_layers):
      d_out = feature_dims[index]
      self.dilated_res_blocks.append(DilatedResidualAttention(d_in, d_out))
      d_in = 2 * d_out

    # build decoder blocks
    d_out = d_in
    self.decoder_0 = conv2d(d_in, d_out, 1, 1, 0)

    # from high to low
    heads = []
    self.decoder_blocks = nn.ModuleList()
    for index in range(num_layers):
      if index < 4:
        d_in = d_out + 2 * feature_dims[-index - 2]
        d_out = 2 * feature_dims[-index - 2]
      else:
        d_in = 4 * feature_dims[-5]
        d_out = 2 * feature_dims[-5]
      self.decoder_blocks.append(conv2d(d_in, d_out, 1, 1, 0))

      # output layer
      head = nn.Sequential(
          conv2d(d_out, 64, 1, 1, 0),
          conv2d(64, 32, 1, 1, 0),
          nn.Dropout(0.5),
          nn.Conv2d(32, num_classes, 1, 1, 0, bias=True))
      heads.append(head)

    # multihead
    self.heads = nn.ModuleList(heads)

  def forward(self, xyz, neigh_idx, sub_idx, interp_idx, features, labels=None):
    """RandLANet

    Args:
        xyz (List[torch.Tensor]):        [16, 3, 16384, 1], [16, 3, 4096, 1], [16, 3, 1024, 1], [16, 3, 256, 1], [16, 3, 64, 1]
        neigh_idx (List[torch.Tensor]):  [16, 16384, 16], [16, 4096, 16], [16, 1024, 16], [16, 256, 16], [16, 64, 16]
        sub_idx (List[torch.Tensor]):    [16, 4096, 16], [16, 1024, 16], [16, 256, 16], [16, 64, 16], [16, 32, 16]
        interp_idx (List[torch.Tensor]): [16, 16384, 1], [16, 4096, 1], [16, 1024, 1], [16, 256, 1], [16, 64, 1]
        features ([torch.Tensor]): [16, 6, 16384]
        labels ([torch.Tensor]): [16, 16384]

    Returns:
        [torch.Tensor]: [16, 16384, 13]
    """
    # [bs, in_channels, num_points, 1]
    features = self.stem(features)
    features = features.unsqueeze(dim=3)

    # encoder path
    # f_encoded:     [16, 32, 16384, 1], [16, 128, 4096, 1], [16, 256, 1024, 1], [16, 512, 256, 1], [16, 1024, 64, 1]
    # f_downsampled: [16, 32, 4096, 1], [16, 128, 1024, 1], [16, 256, 256, 1], [16, 512, 64, 1], [16, 1024, 32, 1]
    f_encoder_list = []
    for i in range(self.num_layers):
      f_encoded = self.dilated_res_blocks[i](features, xyz[i], neigh_idx[i])
      f_downsampled = nearest_max_downsample(f_encoded, sub_idx[i])
      features = f_downsampled
      if i == 0:
        f_encoder_list.append(f_encoded)
      f_encoder_list.append(f_downsampled)

    # bridge: [16, 1024, 32, 1]
    features = self.decoder_0(f_encoder_list[-1])

    # decoder phase
    # f_upsampled:        [16, 1024, 64, 1], [16, 512, 256, 1], [16, 256, 1024, 1], [16, 128, 4096, 1], [16, 32, 16384, 1]
    # f_up_and_bilateral: [16, 1536, 64, 1], [16, 768, 256, 1], [16, 384, 1024, 1], [16, 160, 4096, 1], [16, 64, 16384, 1]
    # f_decoded:          [16, 512, 64, 1], [16, 256, 256, 1], [16, 128, 1024, 1], [16, 32, 4096, 1], [16, 32, 16384, 1]
    f_decoder_list = []
    f_outs, f_labels = [], []
    for i in range(self.num_layers):
      f_upsampled = nearest_upsample(features, interp_idx[-i-1])
      f_up_and_bilateral = torch.cat([f_encoder_list[-i-2], f_upsampled], dim=1)
      f_decoded = self.decoder_blocks[i](f_up_and_bilateral)
      features = f_decoded

      # segmentation head
      f_out = self.heads[i](features)
      f_out = f_out.squeeze(3).transpose(1, 2)
      f_outs.append(f_out)

      # for training
      if labels is not None:
        f_labels.append(torch.gather(labels, dim=1, index=interp_idx[-i-1].squeeze()))

    # for inference
    if labels is None:
      return f_outs[-1]

    # for training
    return f_outs, f_labels
