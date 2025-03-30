import glob
import math
import multiprocessing as mp
import re
import sys
from datetime import datetime as dt

import cv2
import imageio
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib import animation
from numba import njit
from matplotlib import colors


def compress_image(image_path, quality=90):
    # Read the image
    img = cv2.imread(image_path)

    # Encode the image with JPEG compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encoded_img = cv2.imencode('.jpg', img, encode_param)

    # Decode the compressed image
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    return decoded_img


class PlotWithButtonsAndSlider:
    def __init__(self, xmin_0, xmax_0, ymin_0, ymax_0, x_c_0=-0.8, y_c_0=-0.156,
                 height=1000, length=1000, horizon=2e50, fig=None, ax=None, mode='mandelbrot', colormap='jet'):
        self.xmin_0 = xmin_0
        self.xmax_0 = xmax_0
        self.ymin_0 = ymin_0
        self.ymax_0 = ymax_0
        self.x_c_0 = x_c_0
        self.y_c_0 = y_c_0
        self.height = height
        self.length = length
        self.horizon = horizon
        self.fig = fig
        self.ax = ax
        self.mode = mode
        self.colormap = colormap
        self.fig2 = plt.figure(figsize=(6, 0.7))
        self.ax_n = self.fig2.add_axes((0.1, 0.6, 0.77, 0.2))
        self.ax_n_reset = self.fig2.add_axes((0.45, 0.1, 0.11, 0.3))
        self.ax_save = self.fig2.add_axes((0.1, 0.1, 0.11, 0.3))
        self.button_n_reset = Button(self.ax_n_reset, 'Reset', hovercolor='0.975')
        self.button_save = Button(self.ax_save, 'Save', hovercolor='0.975')
        self.slider_move = False
        self.slider_n = Slider(ax=self.ax_n, label="n", valmin=0, valmax=4000, valinit=100, valstep=1)
        if self.mode == 'julia':
            self.fig1 = plt.figure(figsize=(6, 1.5))
            self.ax_xc = self.fig1.add_axes((0.1, 0.7, 0.77, 0.1))
            self.ax_yc = self.fig1.add_axes((0.1, 0.4, 0.77, 0.1))
            self.ax_reset = self.fig1.add_axes((0.45, 0.1, 0.11, 0.2))
            self.button_reset = Button(self.ax_reset, 'Reset', hovercolor='0.975')
            self.slider_xc = Slider(ax=self.ax_xc, label="x_c", valmin=-1, valmax=1, valinit=self.x_c_0)
            self.slider_yc = Slider(ax=self.ax_yc, label="y_c", valmin=-1, valmax=1, valinit=self.y_c_0)

    def make_plot(self):
        self.ax.imshow([[0]], origin="lower", cmap='jet')  # Empty initial image
        self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        self.slider_n.on_changed(self.ax_update_n)
        self.button_n_reset.on_clicked(self.reset_n)
        self.button_save.on_clicked(self.save)
        self.ax.callbacks.connect("xlim_changed", self.ax_update)
        self.ax.callbacks.connect("ylim_changed", self.ax_update)
        if self.mode == 'mandelbrot':
            self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        elif self.mode == 'julia':
            rho = np.sqrt(self.x_c_0 ** 2 + self.y_c_0 ** 2)
            phi = np.arctan2(self.y_c_0, self.x_c_0)
            self.ax_xc.set_title(rf'$c = {self.x_c_0:.3f} i*{self.y_c_0:+.3f} = {rho:.3f} * e^{{{phi:.3f}i}}$')
            # register the update function with each slider
            self.slider_xc.on_changed(self.c_update)
            self.slider_yc.on_changed(self.c_update)
            self.button_reset.on_clicked(self.reset_xy)
            self.ax.set(xlim=(self.xmin_0, self.xmax_0), ylim=(self.ymin_0, self.ymax_0))
        im = self.ax.images[0]
        im.set(clim=(im.get_array().min(), im.get_array().max()))
        self.fig.tight_layout()
        plt.show()

    @property
    def x_c(self):
        return self.slider_xc.val

    @property
    def y_c(self):
        return self.slider_yc.val

    @property
    def n(self):
        if self.slider_move:
            return self.slider_n.val
        else:
            xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
            zoom = (self.xmax_0 - self.xmin_0) / (xmax - xmin)
            return int(100 * (1 + math.log10(zoom)))

    def c_update(self, event):
        self.ax_update(event)
        rho = math.sqrt(self.x_c ** 2 + self.y_c ** 2)
        phi = math.atan2(self.y_c, self.x_c)
        phi = phi + 2 * math.pi * (phi < 0)
        self.ax_xc.set_title(fr'$c = {self.x_c:.3f} {self.y_c:+.3f}i = {rho:.3f} * e^{{{phi: .3f}i}}$')

    def reset_xy(self, event):
        self.slider_xc.reset()
        self.slider_yc.reset()

    def reset_n(self, event):
        self.slider_move = False
        self.slider_n.set_val(self.n)
        self.slider_move = False
        self.ax_update(event)

    def save(self, event):
        xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
        dpi = input('DPI: ')
        name = input('Name: ')
        colormap = input('Colormap: ')
        while True:
            ll = input('Image length: ')
            try:
                ll = int(ll)
                break
            except ValueError:
                pass
        print(f'Current aspect ratio W/L = {(ymin - ymax) / (xmin - xmax):.3f}')
        print(f'Suggested height = {int(float(ll) * (ymin - ymax) / (xmin - xmax)):g}')
        while True:
            ww = input(f'Image height: ')
            try:
                ww = int(ww)
                break
            except ValueError:
                pass
        try:
            plt.get_cmap(colormap)
        except ValueError:
            print(f"Invalid colormap, use current colormap {self.colormap}.")
            colormap = self.colormap
        try:
            dpi = int(dpi)
        except ValueError:
            dpi = 300
        ll = int(ll) * dpi
        ww = int(ww) * dpi
        if self.mode == 'julia':
            _, _, z = julia_set(xmin, xmax, ymin, ymax, x_c=self.x_c, y_c=self.y_c, length=ll, height=ww,
                                n=self.n, horizon=self.horizon)
        elif self.mode == 'mandelbrot':
            _, _, z = mandelbrot_set(xmin, xmax, ymin, ymax, length=ll, height=ww, n=self.n, horizon=self.horizon)
        plt.imsave(fname=name, arr=z.T, dpi=dpi, cmap=colormap)
        print(f"Successfully saved image to '{name}'!")
        plt.show()

    def ax_update_n(self, event):
        self.slider_move = True
        self.ax_update(event)

    def ax_update(self, event):
        self.ax.set_autoscale_on(False)  # Otherwise, infinite loop
        im = self.ax.images[0]
        xmin, xmax, ymin, ymax = np.float64([*self.ax.get_xlim(), *self.ax.get_ylim()])
        print('lims =', xmin, xmax, ymin, ymax)
        if self.mode == 'julia':
            print('x_c, y_c =', self.x_c, self.y_c)
        print('n, diff =', self.n, xmax - xmin, ymax - ymin)
        if self.mode == 'julia':
            im.set(data=julia_set(xmin, xmax, ymin, ymax, horizon=self.horizon,
                                  length=self.length, height=self.height, n=self.n, x_c=self.x_c, y_c=self.y_c)[2].T,
                   extent=(*self.ax.get_xlim(), *self.ax.get_ylim()), cmap=self.colormap)
            self.ax.figure.canvas.draw()
        elif self.mode == 'mandelbrot':
            # light = colors.LightSource(azdeg=315, altdeg=10)  # create a Light Source, coming from somewhere
            # data = mandelbrot_set(xmin, xmax, ymin, ymax, height=1000, length=1000, n=n, horizon=2e50)[2].T
            # data = light.shade(data, cmap=plt.get_cmap('hot'), vert_exag=1.5,
            #                    norm=colors.PowerNorm(0.3), blend_mode='hsv')
            # im.set(data=data, extent=(*ax.get_xlim(), *ax.get_ylim()))
            im.set(data=mandelbrot_set(xmin, xmax, ymin, ymax, horizon=self.horizon,
                                       length=self.length, height=self.height, n=self.n)[2].T,
                   extent=(*self.ax.get_xlim(), *self.ax.get_ylim()), cmap=self.colormap)
            self.ax.figure.canvas.draw_idle()
        print('min, max =', im.get_array().min(), im.get_array().max(), '\n')
        im.set(clim=(im.get_array().min(), im.get_array().max()))


@njit(fastmath=True)
def julia(x, y, n, x_c, y_c, log_horizon, horizon):
    real = x
    imag = y
    for i in range(n):
        if real * real + imag * imag > horizon:
            # return i
            return i - (math.log(0.5 * math.log(real * real + imag * imag)) - log_horizon) / math.log(2)
        real0 = real
        real = real * real - imag * imag + x_c
        imag = 2 * real0 * imag + y_c
    return 0


@njit(parallel=True, fastmath=True)
def julia_set(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon):
    log_horizon = math.log(math.log(horizon))
    r1 = np.linspace(xmin, xmax, length)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((length, height))
    for i in range(length):
        for j in range(height):
            n3[i, j] = julia(r1[i], r2[j], n, x_c, y_c, log_horizon, horizon)
    return r1, r2, n3


@njit(fastmath=True)
def mandelbrot(x, y, n, log_horizon, horizon):
    real = x
    imag = y
    for i in range(n):
        if real * real + imag * imag > horizon:
            # return i
            return i - (np.log(0.5 * np.log(real * real + imag * imag)) - log_horizon) / np.log(2.0)
        real0 = real
        real = real * real - imag * imag + x
        imag = 2 * real0 * imag + y
    return 0


@njit(parallel=True, fastmath=True)
def mandelbrot_set(xmin, xmax, ymin, ymax, height, length, n, horizon):
    log_horizon = math.log(math.log(horizon))
    r1 = np.linspace(xmin, xmax, length)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((length, height))
    for i in range(length):
        for j in range(height):
            n3[i, j] = mandelbrot(r1[i], r2[j], n, log_horizon, horizon)
    return r1, r2, n3


def make_image(xmin, xmax, ymin, ymax, x_c=-0.8, y_c=0.156, mode='mandelbrot',
               horizon=2e50, n=200, length=10, height=10,
               cmap='seismic', save=True, name='Mandelbrot.tiff', dpi=300):
    img_width = dpi * length
    img_height = dpi * height
    if mode == 'mandelbrot':
        x, y, z = mandelbrot_set(xmin, xmax, ymin, ymax,
                                 img_height, img_width, n, horizon)
    elif mode == 'julia':
        x, y, z = julia_set(xmin, xmax, ymin, ymax, x_c, y_c,
                            img_height, img_width, n, horizon)
    # ticks = np.arange(0, img_width, 3 * dpi)
    ticks = np.arange(0, img_width, dpi / 2)
    x_ticks = xmin + (xmax - xmin) * ticks / img_width
    x_ticks = [f'{x:.4f}' for x in x_ticks]
    # fig, ax = plt.subplots(figsize=(length, height))
    fig, ax = plt.subplots()
    ax.set_xticks(ticks, x_ticks, rotation=-45, ha='left')
    y_ticks = ymin + (ymax - ymin) * ticks / img_width
    y_ticks = [f'{x:.4f}' for x in y_ticks]
    ax.set_yticks(ticks, y_ticks)
    plt.imshow(z.T, origin='lower', cmap=cmap)
    plt.tight_layout()
    if save:
        plt.imsave(name, z.T, dpi=dpi, cmap=cmap)
        # plt.savefig(name, dpi=dpi, bbox_inches='tight')
    plt.show()


def main1(mode):
    fig, ax = plt.subplots()
    P = PlotWithButtonsAndSlider(-2, 0.5, -1.25, 1.25, horizon=2e50,
                                 fig=fig, ax=ax, mode=mode, colormap='jet')
    # P = PlotWithButtonsAndSlider(-2, 2, -1.25, 1.25, fig=fig, ax=ax,
    #                              mode=mode, horizon=4, colormap='jet')
    P.make_plot()


def main2():
    start = dt.now()

    x_min, x_max = -1.257255975039769, -1.2572559750396257
    y_min, y_max = 0.3858051643553329, 0.3858051643554954

    x_c = -0.777807810193171
    y_c = 0.131645108003206

    # x_min = x_c - 0.000000001
    # x_max = x_c + 0.000000001
    # y_min = y_c - 0.000000001
    # y_max = y_c + 0.000000001

    print(x_max - x_min)
    print(y_max - y_min)

    # y_c = 0.86
    # x_c = -0.08
    # x_min = x_c - 0.1
    # x_max = x_c + 0.1
    # y_min = y_c - 0.1
    # y_max = y_c + 0.1

    make_image(x_min, x_max, y_min, y_max, horizon=2e50, n=4000, dpi=300, mode='mandelbrot',
               # length=10, height=int(10 * (y_max - y_min) / (x_max - x_min)),
               length=10, height=10,
               save=False, name='Mandelbrot_im_10.tiff', cmap='hot')  # cmap='hot'

    # x_min, x_max = -2.0, 2.0
    # y_min, y_max = -1.25, 1.25
    # length = 10
    # height = int(length * (y_max - y_min) / (x_max - x_min))
    # make_image(x_min, x_max, y_min, y_max, horizon=4, n=100, dpi=1000, mode='julia',
    #            # x_c=-0.8, y_c=0.156,
    #            x_c=-0.7269, y_c=0.1889,
    #            length=length, height=height,
    #            save=True, name='Julia_2.tiff', cmap='hot')  # cmap='hot'
    print(dt.now() - start)


def make_frame(scale, xmin_1, xmax_1, ymin_1, ymax_1, xmin_2, xmax_2, ymin_2, ymax_2,
               dpi, length, height, horizon, i, colormap):
    xmin_3 = (1 - scale) * xmin_1 + scale * xmin_2
    ymin_3 = (1 - scale) * ymin_1 + scale * ymin_2
    xmax_3 = (1 - scale) * xmax_1 + scale * xmax_2
    ymax_3 = (1 - scale) * ymax_1 + scale * ymax_2

    zoom = (xmax_1 - xmin_1) / (xmax_3 - xmin_3)
    n = int(100 * (1 + math.log10(zoom)))

    print(scale, i, n)
    img_width = dpi * length
    img_height = dpi * height

    a = 0.788
    angle = 0
    x_c = a * np.sin(angle)
    y_c = a * np.cos(angle)

    if colormap == 'shade':
        light = colors.LightSource(azdeg=315, altdeg=10)
        data = mandelbrot_set(xmin_3, xmax_3, ymin_3, ymax_3, img_height, img_width, n=n, horizon=horizon)[2].T
        # data = julia_set(xmin_3, xmax_3, ymin_3, ymax_3, x_c, y_c, img_height, img_width, n=n, horizon=horizon)[2].T
        data = light.shade(data, cmap=plt.cm.hot, vert_exag=1.5,
                           norm=colors.PowerNorm(0.3), blend_mode='hsv')
    else:
        _, _, z = mandelbrot_set(xmin_3, xmax_3, ymin_3, ymax_3, img_height, img_width, n=n, horizon=horizon)
    # _, _, z = julia_set(xmin_3, xmax_3, ymin_3, ymax_3, x_c, y_c, img_height, img_width, n=n, horizon=horizon)
    # plt.imsave(f'anim_mandelbrot/image_{i:d}.png', z.T, dpi=dpi, cmap=colormap)
    plt.imsave(f'anim_mandelbrot/image_{i:d}.png', data, dpi=dpi)
    # return z.T
    return


def julia_set_image(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon, dpi, i, colormap):
    print(i)
    img_width = dpi * length
    img_height = dpi * height
    _, _, z = julia_set(xmin, xmax, ymin, ymax, x_c, y_c, img_height, img_width, n, horizon)
    plt.imsave(f'anim_julia/image_{i:d}.png', z.T, dpi=dpi, cmap=colormap)
    # return z.T
    return


def main3(xmin_1, xmax_1, ymin_1, ymax_1, xmin_2, xmax_2, ymin_2, ymax_2,
          horizon, frames, dpi, length, height, colormap):
    if not np.isclose((xmax_1 - xmin_1) / (ymax_1 - ymin_1), (xmax_2 - xmin_2) / (ymax_2 - ymin_2), atol=0.01):
        print((xmax_1 - xmin_1) / (ymax_1 - ymin_1), (xmax_2 - xmin_2) / (ymax_2 - ymin_2))
        raise ValueError('Aspect ratio must be the same.')

    time0 = dt.now()
    scales = 1.0 - np.logspace(0, -50, frames, base=2, dtype=np.longdouble)
    pool = mp.Pool(mp.cpu_count() - 2)
    result = [pool.apply_async(make_frame, args=(scale, xmin_1, xmax_1, ymin_1, ymax_1, xmin_2, xmax_2, ymin_2,
                                                 ymax_2, dpi, length, height, horizon, i, colormap))
              for i, scale in enumerate(scales)]

    im_arr = [res.get() for res in result]
    pool.close()
    pool.join()
    print(dt.now() - time0)
    time0 = dt.now()

    # for i, image in enumerate(im_arr):
    #     fig = plt.figure(figsize=(6, 6), frameon=False)
    #     ax = plt.Axes(fig, [0., 0., 1., 1.])
    #     ax.set_axis_off()
    #     fig.add_axes(ax)
    #     im = ax.imshow(image, cmap=colormap, animated=True, aspect='auto')
    #     plt.savefig(f'image_{i}.pdf')
    #     plt.close(fig)

    # fig = plt.figure(figsize=(6, 6), frameon=False)
    # ax = plt.Axes(fig, [0., 0., 1., 1.])
    # ax.set_axis_off()
    # fig.add_axes(ax)
    # im = ax.imshow(im_arr[0], cmap=colormap, animated=True, aspect='auto')
    #
    # def animate(frame, image):
    #     image.set_array(im_arr[frame])
    #     return image
    #
    # ani = animation.FuncAnimation(fig=fig, func=animate, frames=frames, interval=20, fargs=(im,))
    # # ani.save('Mandelbrot_im_2.mp4', writer='ffmpeg')
    # plt.show()
    # print(dt.now() - time0)


def main5(xmin, xmax, ymin, ymax, height, length, n, horizon, colormap, dpi, frames):
    time0 = dt.now()
    angle = np.linspace(0, 4 * np.pi, frames)
    a = 0.7885
    x_c = a * np.sin(angle)
    y_c = a * np.cos(angle)
    pool = mp.Pool(mp.cpu_count() - 1)

    result = [pool.apply_async(julia_set_image, kwds={'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax,
                                                      'height': height, 'length': length, 'n': n, 'dpi': dpi,
                                                      'horizon': horizon, 'colormap': colormap,
                                                      'x_c': x_cc, 'y_c': y_cc, 'i': i})
              for i, (x_cc, y_cc) in enumerate(zip(x_c, y_c))]

    im_arr = [res.get() for res in result]
    pool.close()
    pool.join()
    print(dt.now() - time0)
    # fig = plt.figure(figsize=(6, 6), frameon=False)
    # # fig, ax = plt.subplots(figsize=(8, 6), frameon=False)
    # ax = plt.Axes(fig, [0., 0., 1., 1.])
    # ax.set_axis_off()
    # fig.add_axes(ax)
    # im = ax.imshow(im_arr[0], cmap=colormap, animated=True, aspect='auto', interpolation='bicubic')
    #
    # def animate(frame, image):
    #     image.set_array(im_arr[frame])
    #     return image
    #
    # ani = animation.FuncAnimation(fig=fig, func=animate, frames=frames, interval=20, fargs=(im,))
    # ani.save('Mandelbrot_im_2.mp4', writer='ffmpeg')
    # # plt.show()
    # print(dt.now() - time0)


if __name__ == '__main__':
    par = sys.argv[1]
    if par == '1':
        mode = sys.argv[2]
        main1(mode)
    elif par == '2':
        main2()
    elif par == '3':
        xmin_1, xmax_1, ymin_1, ymax_1 = -2.0, 0.5, -1.25, 1.25  # Mandelbrot
        # xmin_1, xmax_1, ymin_1, ymax_1 = -2.0, 2.0, -1.25, 1.25  # Julia
        # xmin_2, xmax_2 = -0.5622029654979828, -0.5622029654967909
        # ymin_2, ymax_2 = 0.6428173061353689, 0.6428173061366026
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # xmin_2, xmax_2 = -1.257255975039769, -1.2572559750396257
        # ymin_2, ymax_2 = 0.3858051643553329, 0.3858051643554954
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # xmin_2, xmax_2 = -0.737706890247751, -0.7377068902466386
        # ymin_2, ymax_2 = -0.17445387343397453, -0.17445387343283492
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # SHOULD ALSO TRY!!!
        # xmin_2, xmax_2 = -0.5699761146477447, -0.5699761146473441
        # ymin_2, ymax_2 = 0.5049183778888079, 0.504918377889188
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # AND THIS!!!
        # xmin_2, xmax_2 = -0.15724267657333385, -0.15724267657255195
        # ymin_2, ymax_2 = 1.039345588588977, 1.0393455885896696
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # xmin_2, xmax_2 = 0.3028744748270258, 0.30287447482742563
        # ymin_2, ymax_2 = 0.0243991641051465, 0.024399164105518123
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        # FOR JULIA
        # xmin_2, xmax_2 = -0.08376124014773263, -0.08376124014752595
        # ymin_2, ymax_2 = -0.20055388801100252, -0.20055388801079843
        # ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        xmin_2, xmax_2 = -1.2555518071409488, -1.2555518071406466
        ymin_2, ymax_2 = 0.38273425204474965, 0.3827342520450359
        ymax_2 = ymin_2 + (xmax_2 - xmin_2) * (ymax_1 - ymin_1) / (xmax_1 - xmin_1)

        main3(xmin_1=xmin_1, xmax_1=xmax_1, ymin_1=ymin_1, ymax_1=ymax_1,
              xmin_2=xmin_2, xmax_2=xmax_2, ymin_2=ymin_2, ymax_2=ymax_2, horizon=4,
              frames=1000, dpi=500, length=10, height=10, colormap='hot')
    elif par == '4':
        path, fmt = sys.argv[2], sys.argv[3]
        # path = 'anim1/'
        # List of PNG files
        files = glob.glob(path + 'image_*.png')  # Add your PDF file paths
        image_files = sorted(files, key=lambda x: int(re.search(r'\d+', x[len(path):]).group()))

        # Read first image to get dimensions
        frame = cv2.imread(image_files[0])
        h, w, _ = frame.shape

        if fmt == 'mp4':
            output_mp4 = "output.mp4"
            fps = 30  # Frame rate
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for mp4 format
            out = cv2.VideoWriter(path + output_mp4, fourcc, fps, (w, h))

            # Write images to video
            for img_file in image_files:
                frame = cv2.imread(img_file)  # Read image
                out.write(frame)  # Write frame

            out.release()  # Save and close file
            print(f"Video saved as {path}{output_mp4}")
        elif fmt == 'gif':
            # frames = [cv2.imread(img) for img in image_files[:100]]
            frames = [compress_image(img, quality=1) for img in image_files[500:]]

            output_gif = "output.gif"
            fps = 30

            # Convert the frames into a GIF using imageio
            with imageio.get_writer(output_gif, mode='I', duration=1 / fps) as writer:
                for img in image_files:
                    # for frame in frames:
                    writer.append_data(compress_image(img, quality=1))
                    # writer.append_data(frame)
    elif par == '5':
        main5(-2.5, 2.5, -2, 2, 10, 10, 20, 4, 'magma', 300, 1000)
