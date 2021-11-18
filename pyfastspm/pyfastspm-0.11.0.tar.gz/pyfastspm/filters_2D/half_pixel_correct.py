"""This module implements the half pixel correction"""

import numpy as np
from tqdm import tqdm

from ..fast_movie import FastMovie


def correct_half_pixel_drift(fast_movie: FastMovie, image_range=None):
    ni, nj = fast_movie.data.shape[1:]
    a = np.array([0.5 - j / (2 * (nj - 1)) for j in range(nj)])
    b = np.array([0.5 + j / (2 * (nj - 1)) for j in range(nj)])

    def correct_up_frame(frame_up):
        corr_uf = np.zeros(frame_up.shape, dtype=np.float)
        for i, j in np.ndindex(frame_up.shape):
            if i == 0:
                corr_uf[i, j] = frame_up[i, j]
            else:
                corr_uf[i, j] = a[j] * frame_up[i - 1, j] + b[j] * frame_up[i, j]
        return corr_uf

    def correct_down_frame(frame_down):
        corr_df = np.zeros(frame_down.shape)
        for i, j in np.ndindex(frame_down.shape):
            if i == ni - 1:
                corr_df[i, j] = frame_down[i, j]
            else:
                corr_df[i, j] = a[j] * frame_down[i + 1, j] + b[j] * frame_down[i, j]
        return corr_df

    progress_bar = tqdm(
        list(fast_movie.iter_frames(image_range=image_range)),
        desc="Half pixel drift correction",
        unit="frames",
    )
    for _, channel, frame_id in fast_movie.iter_frames(image_range):
        orig_frame = fast_movie.data[frame_id, :, :]
        if "f" in fast_movie.channels:
            if "u" in channel:
                fast_movie.data[frame_id, :, :] = correct_up_frame(orig_frame)
            elif "d" in channel:
                fast_movie.data[frame_id, :, :] = correct_down_frame(orig_frame)
        elif "b" in fast_movie.channels:
            if "u" in channel:
                fast_movie.data[frame_id, :, :] = correct_down_frame(orig_frame)
            elif "d" in channel:
                fast_movie.data[frame_id, :, :] = correct_up_frame(orig_frame)
        progress_bar.update(1)
    progress_bar.close()
