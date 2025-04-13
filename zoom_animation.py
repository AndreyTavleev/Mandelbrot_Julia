import argparse
import glob
import json
import multiprocessing as mp
import os
import re
from datetime import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

import config as cfg
from fractal_calculation import mandelbrot_julia_set


def make_colourmap(colours_data):
    """Create a custom colourmap from a list of colour data."""
    colours = []
    for item in colours_data:
        pos = float(item['position'])
        r = float(item['r'])
        g = float(item['g'])
        b = float(item['b'])
        colours.append((pos, (r, g, b, 1.0)))  # RGBA
    if colours[0][0] > 0.0:
        colours.insert(0, (0.0, colours[0][1]))  # Reuse first colour
    if colours[-1][0] < 1.0:
        colours.append((1.0, colours[-1][1]))  # Reuse last colour
    colourmap = colors.LinearSegmentedColormap.from_list(name='user_defined_cmap', colors=colours)
    return colourmap


def make_frame(i, scale, xmin_1, xmax_1, ymin_1, ymax_1, xmin_2, xmax_2, ymin_2, ymax_2,
               mode, x_c, y_c, power, n_regime, n_i, n_f, horizon, length, height, colourmap,
               c_regime, freq, shading, azdeg, altdeg, vert_exag, path, frames):
    """Generate a single frame for the zoom animation."""
    xmin_3 = (1 - scale) * xmin_1 + scale * xmin_2
    ymin_3 = (1 - scale) * ymin_1 + scale * ymin_2
    xmax_3 = (1 - scale) * xmax_1 + scale * xmax_2
    ymax_3 = (1 - scale) * ymax_1 + scale * ymax_2

    zoom = (xmax_1 - xmin_1) / (xmax_3 - xmin_3)
    if n_regime == 'static':
        n = n_f
    elif n_f is None:
        n = int(n_i * (1 + np.log10(zoom)))
    else:
        final_zoom = (xmax_1 - xmin_1) / (xmax_2 - xmin_2)
        alpha = (n_f / n_i - 1) / np.log10(final_zoom)
        n = int(n_i * (1 + alpha * np.log10(zoom)))

    print(f'Frame {i + 1} / {frames}')

    data = mandelbrot_julia_set(xmin_3, xmax_3, ymin_3, ymax_3, horizon=horizon,
                                length=length, height=height, n=n,
                                x_c=x_c, y_c=y_c, power=power, mode=mode)[2].T
    if c_regime == 'standard':
        pass
    elif c_regime == 'sin':
        data = (np.sin(data * freq)) ** 2
    if shading:
        light = colors.LightSource(azdeg=azdeg, altdeg=altdeg)
        data = light.shade(data, cmap=plt.get_cmap(colourmap), vert_exag=vert_exag,
                           blend_mode='hsv')
    plt.imsave(path + f'image_{i:d}.png', data,
               cmap=colourmap if not shading else None, origin='lower')


def validate_aspect_ratio(delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height):
    """Validate the aspect ratio of the image and optionally adjust it."""
    initial_ratio = delta_y_1 / delta_x_1
    final_ratio = delta_y_2 / delta_x_2
    image_aspect_ratio = height / length
    if (not np.isclose(initial_ratio, final_ratio, atol=0.05) or
            not np.isclose(initial_ratio, image_aspect_ratio, atol=0.05) or
            not np.isclose(final_ratio, image_aspect_ratio, atol=0.05)):
        print('The aspect ratio should remain the same between the initial and '
              'final frames and the image dimensions.')
        print(f'Initial aspect ratio delta_y / delta_x = {initial_ratio:.3f}')
        print(f'Final aspect ratio delta_y / delta_x = {final_ratio:.3f}')
        print(f'Current dimensions and aspect ratio (L, H, AR) = ({length}, {height}, '
              f'{height / length:.3f})')
        print(f'Suggested dimensions (L, H) = ({length}, {int(float(length) * initial_ratio):g}) or '
              f'({length}, {int(float(length) * final_ratio):g})')
        print(f'Suggested delta_y_2 = {delta_x_2 * initial_ratio}')
        print(f'Or suggested delta_y_1 = {delta_x_1 * final_ratio}')
        print('Do you want to adjust the aspect ratio based on the initial fractal [1], '
              'the final fractal [2], or continue with the current aspect ratio [n]?')
        while True:
            ans = input('Enter 1, 2 or n: ')
            if ans == '1':
                delta_y_2 = delta_x_2 * initial_ratio
                height = int(float(length) * initial_ratio)
                print('Aspect ratio and image size adjusted for the initial fractal')
                return delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height
            elif ans == '2':
                delta_y_1 = delta_x_1 * final_ratio
                height = int(float(length) * final_ratio)
                print('Aspect ratio and image size adjusted for the final fractal')
                return delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height
            elif ans.lower() == 'n':
                print('Keeping the current aspect ratio.')
                return delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height
            else:
                continue
    return delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height


def generate_video(path, name, fps=30):
    """Generate a video from the saved frames."""
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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format
    out = cv2.VideoWriter(path + name, fourcc, fps, (w, h))

    # Write images to video
    for img_file in image_files:
        frame = cv2.imread(img_file)  # Read image
        out.write(frame)  # Write frame

    out.release()  # Save and close file
    print(f"Video saved as {path}{name}")


def main(metadata, x_centre_1, y_centre_1, delta_x_1, delta_y_1,
         x_centre_2, y_centre_2, delta_x_2, delta_y_2, x_c, y_c,
         mode, power, n_regime, n_i, n_f, horizon, frames, length, height, colourmap,
         c_regime, freq, shading, azdeg, altdeg, vert_exag, threads, path):
    """Main function to generate the zoom animation."""
    if not isinstance(colourmap, str):
        colourmap = make_colourmap(colourmap)
    if metadata:
        with open(metadata, 'r') as f:
            metadata = json.load(f)
        xmin_2, xmax_2 = metadata['lims_x']
        ymin_2, ymax_2 = metadata['lims_y']
        delta_x_2 = xmax_2 - xmin_2
        delta_y_2 = ymax_2 - ymin_2
        x_centre_2 = xmin_2 + delta_x_2 / 2
        y_centre_2 = ymin_2 + delta_y_2 / 2
        mode = metadata['mode']
        if mode == 'julia':
            x_c = metadata['x_c']
            y_c = metadata['y_c']
        horizon = metadata['horizon']
        power = metadata['power']
        n_f = metadata['n']
        shading = metadata['shading']
        if shading:
            azdeg = metadata['azdeg']
            altdeg = metadata['altdeg']
            vert_exag = metadata['vert_exag']
            azdeg = max(0.0, min(360.0, azdeg))
            altdeg = max(0.0, min(90.0, altdeg))
        c_regime = metadata['regime']
        if c_regime == 'sin':
            freq = metadata['freq']
        if isinstance(metadata['colourmap'], str):
            colourmap = metadata['colourmap']
        else:
            colourmap = make_colourmap(metadata['colourmap'])

    delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height = validate_aspect_ratio(
        delta_x_1, delta_y_1, delta_x_2, delta_y_2, length, height)
    xmin_1 = x_centre_1 - delta_x_1 / 2
    xmax_1 = x_centre_1 + delta_x_1 / 2
    ymin_1 = y_centre_1 - delta_y_1 / 2
    ymax_1 = y_centre_1 + delta_y_1 / 2

    xmin_2 = x_centre_2 - delta_x_2 / 2
    xmax_2 = x_centre_2 + delta_x_2 / 2
    ymin_2 = y_centre_2 - delta_y_2 / 2
    ymax_2 = y_centre_2 + delta_y_2 / 2

    time0 = dt.now()
    scales = 1.0 - np.logspace(0, -50, frames, base=2, dtype=np.float64)
    pool = mp.Pool(threads)
    result = [pool.apply_async(make_frame, args=(i, scale, xmin_1, xmax_1, ymin_1, ymax_1, xmin_2, xmax_2,
                                                 ymin_2, ymax_2, mode, x_c, y_c, power, n_regime, n_i, n_f, horizon,
                                                 length, height, colourmap, c_regime, freq, shading, azdeg,
                                                 altdeg, vert_exag, path, frames))
              for i, scale in enumerate(scales)]

    im_arr = [res.get() for res in result]
    pool.close()
    pool.join()
    print('Completed in:', dt.now() - time0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates a zoom animation of a fractal (Mandelbrot or Julia set), '
                    'with optional shading, colour mapping, and custom calculation and view parameters.',
        epilog='For further information, see the README.md.')
    parser.add_argument('--metadata', type=str,
                        help='Path to the JSON metadata file for loading the fractal configurations. '
                             'The coordinates of the final fractal, fractal calculation parameters '
                             '(particularly, the number of iterations) and colour settings '
                             'will be loaded from this file.')
    parser.add_argument('--x_centre_1', type=np.float64, default=-0.75,
                        help='X-coordinate of the centre for the initial fractal (default: -0.75).')
    parser.add_argument('--y_centre_1', type=np.float64, default=0.0,
                        help='Y-coordinate of the centre for the initial fractal (default: 0.0).')
    parser.add_argument('--delta_x_1', type=np.float64, default=2.5,
                        help='Length of the initial view in the X direction (default: 2.5).')
    parser.add_argument('--delta_y_1', type=np.float64, default=2.5,
                        help='Height of the initial view in the Y direction (default: 2.5).')
    parser.add_argument('--x_centre_2', type=np.float64, default=-0.7380470008824890,
                        help='X-coordinate of the centre for a zoomed-in fractal (default: 0.7380470008824890).')
    parser.add_argument('--y_centre_2', type=np.float64, default=0.1521486399947802,
                        help='Y-coordinate of the centre for a zoomed-in fractal (default: 0.1521486399947802).')
    parser.add_argument('--delta_x_2', type=np.float64, default=0.0000000000008533,
                        help='Length of the final zoomed view in the X direction (default: 0.0000000000008533).')
    parser.add_argument('--delta_y_2', type=np.float64, default=0.0000000000008533,
                        help='Height of the final zoomed view in the Y direction (default: 0.0000000000008533).')
    parser.add_argument('--x_c', type=float, default=cfg.DEFAULT_X_C,
                        help=f'Real part of the Julia set C-parameter (default: {cfg.DEFAULT_X_C}).')
    parser.add_argument('--y_c', type=float, default=cfg.DEFAULT_Y_C,
                        help=f'Imaginary part of the Julia set C-parameter (default: {cfg.DEFAULT_Y_C}).')
    parser.add_argument('-m', '--mode', type=str, default=cfg.DEFAULT_MODE,
                        choices=['mandelbrot', 'julia'],
                        help=f"The fractal type: 'mandelbrot' or 'julia' (default: {cfg.DEFAULT_MODE}).")
    parser.add_argument('-p', '--power', type=int, default=cfg.DEFAULT_POWER,
                        choices=[2, 3, 4, 5, 6, 7, 8],
                        help=f'Power/exponent used in the fractal formula: 2...8 (default: {cfg.DEFAULT_POWER}).')
    parser.add_argument('--n_regime', type=str, default='dynamic',
                        choices=['dynamic', 'static'],
                        help='Dynamic or static number of iterations for the fractal calculation (default: dynamic).')
    parser.add_argument('--n_i', type=int, default=100,
                        help="Number of iterations for the initial fractal (default: 100). "
                             "If n_regime is 'static', parameter n_i is ignored.")
    parser.add_argument('--n_f', type=int,
                        help="Number of iterations for the final zoomed-in fractal. "
                             "If not provided, and n_regime is 'dynamic', it will be calculated "
                             "dynamically based on the zoom level. If n_regime is 'static', it defaults to 1000. "
                             "If metadata is provided, the number of iterations will be taken from there.")
    parser.add_argument('-H', '--horizon', type=np.float64,
                        help=f'Divergence threshold (horizon) for the fractal calculation. '
                             f'(default: {cfg.DEFAULT_HORIZON_MANDELBROT} for mandelbrot and'
                             f'{cfg.DEFAULT_HORIZON_JULIA} for julia).')
    parser.add_argument('-f', '--frames', type=int, default=400,
                        help='Number of frames to render for the animation (default: 400).')
    parser.add_argument('-l', '--length', type=int, default=cfg.DEFAULT_LENGTH,
                        help=f'Image width in inches (default: {cfg.DEFAULT_LENGTH}).')
    parser.add_argument('-hei', '--height', type=int, default=cfg.DEFAULT_HEIGHT,
                        help=f'Image width in inches (default: {cfg.DEFAULT_LENGTH}).')
    parser.add_argument('-c', '--colourmap', type=str, default=cfg.DEFAULT_COLOURMAP,
                        help=f'Name of the colourmap to use or the path to a JSON file containing '
                             f'a colourmap definition (default: {cfg.DEFAULT_COLOURMAP}).')
    parser.add_argument('--c_regime', type=str, default=cfg.DEFAULT_REGIME,
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
    if args.horizon is None:
        if args.mode == 'mandelbrot':
            args.horizon = cfg.DEFAULT_HORIZON_MANDELBROT
        else:
            args.horizon = cfg.DEFAULT_HORIZON_JULIA
    if args.n_f is None:
        if args.n_regime == 'static':
            args.n_f = 1000
        else:
            args.n_f = None
    path = input('Enter the path to the folder where the frames and video will be saved (default: tmp/): ')
    if not path:
        path = 'tmp/'
    if path[-1] != '/':
        path += '/'
    os.makedirs(path, exist_ok=True)
    main(**vars(args), path=path)
    video_name = input('Enter the name for the video (default: output.mp4): ')

    generate_video(path, video_name)
