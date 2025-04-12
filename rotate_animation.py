import argparse
import glob
import json
import multiprocessing as mp
import os
import re
import warnings
from datetime import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

import config as cfg
from Mandelbrot_Julia import mandelbrot_julia_set


def make_colourmap(colours_data):
    colours = []
    for pos, colour in colours_data:
        r = round(float(colour['r']))
        g = round(float(colour['g']))
        b = round(float(colour['b']))
        colours.append((pos, r, g, b, 1.0))  # RGBA
    if colours[0][0] > 0.0:
        colours.insert(0, (0.0, colours[0][1]))  # Reuse first colour
    if colours[-1][0] < 1.0:
        colours.append((1.0, colours[-1][1]))  # Reuse last colour
    colourmap = colors.LinearSegmentedColormap.from_list(name='user_defined_cmap', colors=colours)
    return colourmap


def make_frame(i, xmin, xmax, ymin, ymax, x_c, y_c, n, power, horizon, length, height,
               colourmap, regime, freq, shading, azdeg, altdeg, vert_exag, path, frames):
    # print(scale, i, n)
    print(f'Frame {i} / {frames}')

    data = mandelbrot_julia_set(xmin, xmax, ymin, ymax, horizon=horizon,
                                length=length, height=height, n=n,
                                x_c=x_c, y_c=y_c, power=power, mode='julia')[2].T
    if regime == 'standard':
        pass
    elif regime == 'sin':
        data = (np.sin(data * freq)) ** 2
    if shading:
        light = colors.LightSource(azdeg=azdeg, altdeg=altdeg)
        data = light.shade(data, cmap=plt.get_cmap(colourmap), vert_exag=vert_exag,
                           blend_mode='hsv')
        plt.imsave(path + f'image_{i:d}.png', data, origin='lower')
    else:
        plt.imsave(path + f'image_{i:d}.png', data,
                   cmap=colourmap, origin='lower')
    return


def main(metadata, xmin, xmax, ymin, ymax, rho, phi_min, phi_max, n, power,
         horizon, frames, length, height, colourmap,
         regime, freq, shading, azdeg, altdeg, vert_exag, threads, path):
    if not isinstance(colourmap, str):
        colourmap = make_colourmap(colourmap)
    if metadata:
        with open(metadata, 'r') as f:
            metadata = json.load(f)
        xmin, xmax = metadata['lims_x']
        ymin, ymax = metadata['lims_y']
        mode = metadata['mode']
        if mode == 'julia':
            rho = np.sqrt(metadata['x_c'] ** 2 + metadata['y_c'] ** 2)
        else:
            if rho:
                warnings.warn("Metadata file contains Mandelbrot set. The 'rho' parameter "
                              "has been set separately by user.")
            else:
                warnings.warn("Metadata file contains Mandelbrot set. Use default 'rho' parameter.")
        horizon = metadata['horizon']
        power = metadata['power']
        shading = metadata['shading']
        if shading:
            azdeg = metadata['azdeg']
            altdeg = metadata['altdeg']
            vert_exag = metadata['vert_exag']
            azdeg = max(0.0, min(360.0, azdeg))
            altdeg = max(0.0, min(90.0, altdeg))
        regime = metadata['regime']
        if regime == 'sin':
            freq = metadata['freq']
        if isinstance(metadata['colourmap'], str):
            colourmap = metadata['colourmap']
        else:
            colourmap = make_colourmap(metadata['colourmap'])

    if not np.isclose((ymax - ymin) / (xmax - xmin), height / length, atol=0.05):
        warnings.warn('The aspect ratio should remain the same for axes and image size.')
        print(f'Aspect ratio = {(ymax - ymin) / (xmax - xmin):.3f}')
        print(f'L, H = {length}, {height}')
        print(
            f'Suggested L, H = {length}, {int(float(length) * (ymax - ymin) / (xmax - xmin)):g}')
        while True:
            ans = input('Continue to draw with the current aspect ratio? [y/n] ')
            if ans.lower() == 'y':
                break
            elif ans.lower() == 'n':
                return
            else:
                print('Please enter y or n.')
                continue

    time0 = dt.now()
    angle = np.linspace(phi_min, phi_max, frames)
    x_c = rho * np.sin(angle)
    y_c = rho * np.cos(angle)
    pool = mp.Pool(threads)

    result = [pool.apply_async(make_frame, kwds={'i': i, 'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax,
                                                 'x_c': x_cc, 'y_c': y_cc, 'n': n, 'power': power,
                                                 'horizon': horizon, 'length': length, 'height': height,
                                                 'colourmap': colourmap, 'regime': regime, 'freq': freq,
                                                 'shading': shading, 'azdeg': azdeg, 'altdeg': altdeg,
                                                 'vert_exag': vert_exag, 'path': path, 'frames': frames})
              for i, (x_cc, y_cc) in enumerate(zip(x_c, y_c))]

    im_arr = [res.get() for res in result]
    pool.close()
    pool.join()
    print('Completed in:', dt.now() - time0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates a rotational animation of a Julia set, '
                    'with optional shading, colour mapping, and custom calculation and view parameters.',
        epilog='For further information, see the README.md.')
    parser.add_argument('--metadata', type=str,
                        help='Path to the JSON metadata file for loading the fractal configurations. '
                             'The coordinates of the fractal, fractal calculation parameters '
                             'and colour settings will be loaded from this file.')
    parser.add_argument('--xmin', type=np.float64, default=-2.0,
                        help='X-axis left bound (default: -2.0).')
    parser.add_argument('--xmax', type=np.float64, default=2.0,
                        help='X-axis right bound (default: 2.0).')
    parser.add_argument('--ymin', type=np.float64, default=-2.0,
                        help='Y-axis left bound (default: -2.0).')
    parser.add_argument('--ymax', type=np.float64, default=2.0,
                        help='Y-axis right bound (default: 2.0).')
    parser.add_argument('--rho', type=float, default=0.788,
                        help=f"Modulus 'rho' of the Julia set C-parameter (default: 0.788).")
    parser.add_argument('--phi_min', type=float, default=0.0,
                        help=f"Minimum argument 'phi' of the Julia set C-parameter (default: 0.0).")
    parser.add_argument('--phi_max', type=float, default=2 * np.pi,
                        help=f"Maximum argument 'phi' of the Julia set C-parameter (default: 2pi).")
    parser.add_argument('--n', type=float, default=100,
                        help=f"Iteration limit for the fractal calculation (default: 100).")
    parser.add_argument('-p', '--power', type=int, default=cfg.DEFAULT_POWER,
                        choices=[2, 3, 4, 5, 6, 7, 8],
                        help=f'Power/exponent used in the fractal formula: 2...8 (default: {cfg.DEFAULT_POWER}).')
    parser.add_argument('-H', '--horizon', type=np.float64, default=cfg.DEFAULT_HORIZON_JULIA,
                        help=f'Divergence threshold (horizon) for the fractal calculation. '
                             f'(default: {cfg.DEFAULT_HORIZON_JULIA}).')
    parser.add_argument('-f', '--frames', type=int, default=400,
                        help='Number of frames to render for the animation (default: 400).')
    parser.add_argument('-l', '--length', type=int, default=cfg.DEFAULT_LENGTH,
                        help=f'Image width in inches (default: {cfg.DEFAULT_LENGTH}).')
    parser.add_argument('-hei', '--height', type=int, default=cfg.DEFAULT_HEIGHT,
                        help=f'Image width in inches (default: {cfg.DEFAULT_LENGTH}).')
    parser.add_argument('-c', '--colourmap', type=str, default=cfg.DEFAULT_COLOURMAP,
                        help=f'Name of the colourmap to use or the path to a JSON file containing '
                             f'a colourmap definition (default: {cfg.DEFAULT_COLOURMAP}).')
    parser.add_argument('-r', '--regime', type=str, default=cfg.DEFAULT_REGIME,
                        choices=['standard', 'sin'],
                        help=f"The colouring regime: 'standard' or 'sin' (default: {cfg.DEFAULT_REGIME}).")
    parser.add_argument('-fr', '--freq', type=float, default=cfg.DEFAULT_FREQ,
                        help=f"Frequency for 'sin' colour regime (default: {cfg.DEFAULT_FREQ}).")
    parser.add_argument('-s', '--shading', action='store_true',
                        help='Enable 3D-like surface shading (hillshading).')
    parser.add_argument('-az', '--azdeg', type=float, default=315,
                        help='Azimuth angle in degrees for light source direction in shading (default: 315).')
    parser.add_argument('-al', '--altdeg', type=float, default=10,
                        help='Altitude angle in degrees for the light source in shading (default: 10).')
    parser.add_argument('-ve', '--vert_exag', type=float, default=1.0,
                        help='Vertical exaggeration factor for shading relief (default: 1.0).')
    parser.add_argument('-t', '--threads', type=int, default=mp.cpu_count() - 2,
                        help='Number of threads to use for frame creation (default: number of CPU cores - 2).')
    args = parser.parse_args()
    path = input('Enter the path to the folder where the frames and video will be saved (default: tmp/): ')
    if not path:
        path = 'tmp/'
    if path[-1] != '/':
        path += '/'
    os.makedirs(path, exist_ok=True)
    main(**vars(args), path=path)
    name = input('Enter the name for the video (default: output.mp4): ')

    import cv2

    # List of PNG files
    files = glob.glob(path + 'image_*.png')
    image_files = sorted(files, key=lambda x: int(
        re.search(r'\d+', x[len(path):]).group()))

    # Read first image to get dimensions
    frame = cv2.imread(image_files[0])
    h, w, _ = frame.shape

    if not name:
        name = 'output.mp4'
    if name[-4:] != '.mp4':
        name += '.mp4'
    fps = 30  # Frame rate
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format
    out = cv2.VideoWriter(path + name, fourcc, fps, (w, h))

    # Write images to video
    for img_file in image_files:
        frame = cv2.imread(img_file)  # Read image
        out.write(frame)  # Write frame

    out.release()  # Save and close file
    print(f"Video saved as {path}{name}")
