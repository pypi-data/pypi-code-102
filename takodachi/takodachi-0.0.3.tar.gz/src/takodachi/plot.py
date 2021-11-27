"""Routines for plotting"""

from os.path import isfile, splitext

from PIL import Image, ImageDraw
import numpy as np

def data2axes(ax, coord):
    return ax.transAxes.inverted().transform(ax.transData.transform(coord))

def data4_to_axes4(ax, data4):
    d4 = np.asarray(data4)
    a4 = data2axes(ax, d4[:2])
    a4p = data2axes(ax, d4[:2] + d4[2:])
    return np.concatenate((a4, a4p - a4))



def round_image(fpath, out_fpath=None, verbose=False):
    
    #### Load given image
    if not isfile: raise Exception("File not found : '{}'".format(fpath))
    img = Image.open(fpath).convert("RGB")
    img_rgb_arr = np.array(img)

    #### Prepare masked alpha
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    h, w = img.size
    draw.pieslice([0,0,h,w], 0, 360, fill=255)
    alpha_arr = np.array(alpha)
    img_rgba_arr = np.dstack((img_rgb_arr,alpha_arr))
    
    img_rgba = Image.fromarray(img_rgba_arr)

    if out_fpath is not None:
        if verbose: print("Saving '{}'".format(out_fpath))
        img_rgba.save(out_fpath)

    return img_rgba_arr

