import math
from random import uniform

import numpy as np
from numba import njit


@njit(fastmath=True, inline='always')
def _init_c_mandelbrot_burning_ship(x, y, x_c, y_c):
    return x, y


@njit(fastmath=True, inline='always')
def _init_c_julia_burning_ship_julia(x, y, x_c, y_c):
    return x_c, y_c


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_2(real, imag, x_c, y_c):
    real0 = real
    real = real * real - imag * imag + x_c
    imag = 2 * real0 * imag + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_3(real, imag, x_c, y_c):
    real0 = real
    real = real * real * real - 3 * real * imag * imag + x_c
    imag = 3 * real0 * real0 * imag - imag * imag * imag + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_4(real, imag, x_c, y_c):
    real0 = real
    real = real * real * real * real - 6 * real * real * imag * imag + imag * imag * imag * imag + x_c
    imag = 4 * (real0 * real0 * real0 * imag - real0 * imag * imag * imag) + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_5(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real - 10 * real * real * real * imag * imag +
            5 * real * imag * imag * imag * imag + x_c)
    imag = (imag * imag * imag * imag * imag - 10 * real0 * real0 * imag * imag * imag +
            5 * real0 * real0 * real0 * real0 * imag + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_6(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real * real - imag * imag * imag * imag * imag * imag +
            15 * (real * real * imag * imag * imag * imag - real * real * real * real * imag * imag) + x_c)
    imag = (6 * (real0 * real0 * real0 * real0 * real0 * imag + real0 * imag * imag * imag * imag * imag) -
            20 * real0 * real0 * real0 * imag * imag * imag + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_7(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real * real * real -
            21 * real * real * real * real * real * imag * imag +
            35 * real * real * real * imag * imag * imag * imag -
            7 * real * imag * imag * imag * imag * imag * imag + x_c)
    imag = (7 * real0 * real0 * real0 * real0 * real0 * real0 * imag -
            35 * real0 * real0 * real0 * real0 * imag * imag * imag +
            21 * real0 * real0 * imag * imag * imag * imag * imag -
            imag * imag * imag * imag * imag * imag * imag + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_mandelbrot_julia_8(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real * real * real * real +
            imag * imag * imag * imag * imag * imag * imag * imag -
            28 * (real * real * real * real * real * real * imag * imag +
                  real * real * imag * imag * imag * imag * imag * imag) +
            70 * real * real * real * real * imag * imag * imag * imag + x_c)
    imag = (8 * (real0 * real0 * real0 * real0 * real0 * real0 * real0 * imag -
                 real0 * imag * imag * imag * imag * imag * imag * imag) +
            56 * (real0 * real0 * real0 * imag * imag * imag * imag * imag -
                  real0 * real0 * real0 * real0 * real0 * imag * imag * imag) + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_2(real, imag, x_c, y_c):
    real0 = real
    real = real * real - imag * imag + x_c
    imag = 2 * abs(real0 * imag) + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_3(real, imag, x_c, y_c):
    real0 = real
    real = abs(real * real * real) - 3 * abs(real * imag * imag) + x_c
    imag = 3 * abs(real0 * real0 * imag) - abs(imag * imag * imag) + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_4(real, imag, x_c, y_c):
    real0 = real
    real = real * real * real * real - 6 * real * real * imag * imag + imag * imag * imag * imag + x_c
    imag = 4 * (abs(real0 * real0 * real0 * imag) - abs(real0 * imag * imag * imag)) + y_c
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_5(real, imag, x_c, y_c):
    real0 = real
    real = (abs(real * real * real * real * real) - 10 * abs(real * real * real * imag * imag) +
            5 * abs(real * imag * imag * imag * imag) + x_c)
    imag = (abs(imag * imag * imag * imag * imag) - 10 * abs(real0 * real0 * imag * imag * imag) +
            5 * abs(real0 * real0 * real0 * real0 * imag) + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_6(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real * real - imag * imag * imag * imag * imag * imag +
            15 * (real * real * imag * imag * imag * imag - real * real * real * real * imag * imag) + x_c)
    imag = (6 * (abs(real0 * real0 * real0 * real0 * real0 * imag) +
                 abs(real0 * imag * imag * imag * imag * imag)) -
            20 * abs(real0 * real0 * real0 * imag * imag * imag) + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_7(real, imag, x_c, y_c):
    real0 = real
    real = (abs(real * real * real * real * real * real * real) -
            21 * abs(real * real * real * real * real * imag * imag) +
            35 * abs(real * real * real * imag * imag * imag * imag) -
            7 * abs(real * imag * imag * imag * imag * imag * imag) + x_c)
    imag = (7 * abs(real0 * real0 * real0 * real0 * real0 * real0 * imag) -
            35 * abs(real0 * real0 * real0 * real0 * imag * imag * imag) +
            21 * abs(real0 * real0 * imag * imag * imag * imag * imag) -
            abs(imag * imag * imag * imag * imag * imag * imag) + y_c)
    return real, imag


@njit(fastmath=True, inline='always')
def _update_burning_ship_8(real, imag, x_c, y_c):
    real0 = real
    real = (real * real * real * real * real * real * real * real +
            imag * imag * imag * imag * imag * imag * imag * imag -
            28 * (real * real * real * real * real * real * imag * imag +
                  real * real * imag * imag * imag * imag * imag * imag) +
            70 * real * real * real * real * imag * imag * imag * imag + x_c)
    imag = (8 * (abs(real0 * real0 * real0 * real0 * real0 * real0 * real0 * imag) -
                 abs(real0 * imag * imag * imag * imag * imag * imag * imag)) +
            56 * (abs(real0 * real0 * real0 * imag * imag * imag * imag * imag) -
                  abs(real0 * real0 * real0 * real0 * real0 * imag * imag * imag)) + y_c)
    return real, imag


@njit(parallel=True, fastmath=True)
def fractal_set(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon, power=2, mode='mandelbrot'):
    log_horizon = math.log(math.log(horizon))
    r1 = np.linspace(xmin, xmax, length)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((length, height))

    if mode in {'mandelbrot', 'burning_ship'}:
        init_c = _init_c_mandelbrot_burning_ship
    elif mode in {'julia', 'burning_ship_julia'}:
        init_c = _init_c_julia_burning_ship_julia
    else:
        raise ValueError('Mode must be mandelbrot, julia, burning_ship, or burning_ship_julia.')

    if mode in {'mandelbrot', 'julia'} and power == 2:
        update = _update_mandelbrot_julia_2
    elif mode in {'mandelbrot', 'julia'} and power == 3:
        update = _update_mandelbrot_julia_3
    elif mode in {'mandelbrot', 'julia'} and power == 4:
        update = _update_mandelbrot_julia_4
    elif mode in {'mandelbrot', 'julia'} and power == 5:
        update = _update_mandelbrot_julia_5
    elif mode in {'mandelbrot', 'julia'} and power == 6:
        update = _update_mandelbrot_julia_6
    elif mode in {'mandelbrot', 'julia'} and power == 7:
        update = _update_mandelbrot_julia_7
    elif mode in {'mandelbrot', 'julia'} and power == 8:
        update = _update_mandelbrot_julia_8
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 2:
        update = _update_burning_ship_2
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 3:
        update = _update_burning_ship_3
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 4:
        update = _update_burning_ship_4
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 5:
        update = _update_burning_ship_5
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 6:
        update = _update_burning_ship_6
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 7:
        update = _update_burning_ship_7
    elif mode in {'burning_ship', 'burning_ship_julia'} and power == 8:
        update = _update_burning_ship_8
    else:
        raise ValueError('Power must be between 2 and 8.')

    for i in range(length):
        for j in range(height):
            real = r1[i]
            imag = r2[j]
            x_0, y_0 = init_c(real, imag, x_c, y_c)
            val = 0.0
            for iteration in range(n):
                if real * real + imag * imag > horizon:
                    val = (iteration + 1 -
                           (math.log(math.log(real * real + imag * imag)) - log_horizon) / math.log(float(power)))
                    break
                real, imag = update(real, imag, x_0, y_0)
            n3[i, j] = val
    return r1, r2, n3


@njit(fastmath=True, parallel=True)
def buddhabrot_set(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon, power=2, mode='mandelbrot'):
    samples = 10_000_000
    r1 = [1]
    r2 = [1]
    n3 = np.zeros((length, height))

    if mode == 'mandelbrot':
        init_c = _init_c_mandelbrot_burning_ship
    elif mode == 'julia':
        init_c = _init_c_julia_burning_ship_julia
    else:
        raise ValueError('Mode must be mandelbrot or julia.')

    if mode in {'mandelbrot', 'julia'} and power == 2:
        update = _update_mandelbrot_julia_2
    elif mode in {'mandelbrot', 'julia'} and power == 3:
        update = _update_mandelbrot_julia_3
    elif mode in {'mandelbrot', 'julia'} and power == 4:
        update = _update_mandelbrot_julia_4
    elif mode in {'mandelbrot', 'julia'} and power == 5:
        update = _update_mandelbrot_julia_5
    elif mode in {'mandelbrot', 'julia'} and power == 6:
        update = _update_mandelbrot_julia_6
    elif mode in {'mandelbrot', 'julia'} and power == 7:
        update = _update_mandelbrot_julia_7
    elif mode in {'mandelbrot', 'julia'} and power == 8:
        update = _update_mandelbrot_julia_8
    else:
        raise ValueError('Power must be between 2 and 8.')

    for _ in range(samples):
        real = uniform(xmin, xmax)
        imag = uniform(ymin, ymax)
        orbit = []

        x_0, y_0 = init_c(real, imag, x_c, y_c)

        for i in range(n):
            if real * real + imag * imag > horizon:
                break
            real, imag = update(real, imag, x_0, y_0)
            orbit.append((real, imag))
        else:
            continue
        if len(orbit) > 50:
            for (real, imag) in orbit:
                if xmin <= real < xmax and ymin <= imag < ymax:
                    i = int((real - xmin) / (xmax - xmin) * length)
                    j = int((imag - ymin) / (ymax - ymin) * height)
                    n3[i, j] += 1
    return r1, r2, n3
