import math

import numpy as np
from numba import njit


@njit(fastmath=True)
def mandelbrot_julia(x, y, n, x_c, y_c, log_horizon, horizon, power=2, mode='mandelbrot'):
    real = x
    imag = y
    if mode == 'mandelbrot':
        x_c, y_c = x, y
    for i in range(n):
        if real * real + imag * imag > horizon:
            # return i
            return i + 2 - (math.log(math.log(real * real + imag * imag)) - log_horizon) / math.log(float(power))
        real0 = real
        if power == 2:
            real = real * real - imag * imag + x_c
            imag = 2 * real0 * imag + y_c
        elif power == 3:
            real = real * real * real - 3 * real * imag * imag + x_c
            imag = 3 * real0 * real0 * imag - imag * imag * imag + y_c
        elif power == 4:
            real = real * real * real * real - 6 * real * real * imag * imag + imag * imag * imag * imag + x_c
            imag = 4 * (real0 * real0 * real0 * imag - real0 * imag * imag * imag) + y_c
        elif power == 5:
            real = (real * real * real * real * real - 10 * real * real * real * imag * imag +
                    5 * real * imag * imag * imag * imag + x_c)
            imag = (imag * imag * imag * imag * imag - 10 * real0 * real0 * imag * imag * imag +
                    5 * real0 * real0 * real0 * real0 * imag + y_c)
        elif power == 6:
            real = (real * real * real * real * real * real - imag * imag * imag * imag * imag * imag +
                    15 * (real * real * imag * imag * imag * imag - real * real * real * real * imag * imag) + x_c)
            imag = (6 * (real0 * real0 * real0 * real0 * real0 * imag + real0 * imag * imag * imag * imag * imag) -
                    20 * real0 * real0 * real0 * imag * imag * imag + y_c)
        elif power == 7:
            real = (real * real * real * real * real * real * real -
                    21 * real * real * real * real * real * imag * imag +
                    35 * real * real * real * imag * imag * imag * imag -
                    7 * real * imag * imag * imag * imag * imag * imag + x_c)
            imag = (7 * real0 * real0 * real0 * real0 * real0 * real0 * imag -
                    35 * real0 * real0 * real0 * real0 * imag * imag * imag +
                    21 * real0 * real0 * imag * imag * imag * imag * imag -
                    imag * imag * imag * imag * imag * imag * imag + y_c)
        elif power == 8:
            real = (real * real * real * real * real * real * real * real +
                    imag * imag * imag * imag * imag * imag * imag * imag -
                    28 * (real * real * real * real * real * real * imag * imag +
                          real * real * imag * imag * imag * imag * imag * imag) +
                    70 * real * real * real * real * imag * imag * imag * imag + x_c)
            imag = (8 * (real0 * real0 * real0 * real0 * real0 * real0 * real0 * imag -
                         real0 * imag * imag * imag * imag * imag * imag * imag) +
                    56 * (real0 * real0 * real0 * imag * imag * imag * imag * imag -
                          real0 * real0 * real0 * real0 * real0 * imag * imag * imag) + y_c)
        else:
            raise ValueError('Power must be between 2 and 8.')
    return 0


@njit(fastmath=True)
def burning_ship(x, y, n, x_c, y_c, log_horizon, horizon, power=2, mode='burning_ship'):
    real = x
    imag = y
    if mode == 'burning_ship':
        x_c, y_c = x, y
    for i in range(n):
        if real * real + imag * imag > horizon:
            # return i
            return i + 2 - (math.log(math.log(real * real + imag * imag)) - log_horizon) / math.log(float(power))
        real0 = real
        if power == 2:
            real = real * real - imag * imag + x_c
            imag = 2 * abs(real0 * imag) + y_c
        elif power == 3:
            real = abs(real * real * real) - 3 * abs(real * imag * imag) + x_c
            imag = 3 * abs(real0 * real0 * imag) - abs(imag * imag * imag) + y_c
        elif power == 4:
            real = real * real * real * real - 6 * real * real * imag * imag + imag * imag * imag * imag + x_c
            imag = 4 * (abs(real0 * real0 * real0 * imag) - abs(real0 * imag * imag * imag)) + y_c
        elif power == 5:
            real = (abs(real * real * real * real * real) - 10 * abs(real * real * real * imag * imag) +
                    5 * abs(real * imag * imag * imag * imag) + x_c)
            imag = (abs(imag * imag * imag * imag * imag) - 10 * abs(real0 * real0 * imag * imag * imag) +
                    5 * abs(real0 * real0 * real0 * real0 * imag) + y_c)
        elif power == 6:
            real = (real * real * real * real * real * real - imag * imag * imag * imag * imag * imag +
                    15 * (real * real * imag * imag * imag * imag - real * real * real * real * imag * imag) + x_c)
            imag = (6 * (abs(real0 * real0 * real0 * real0 * real0 * imag) +
                         abs(real0 * imag * imag * imag * imag * imag)) -
                    20 * abs(real0 * real0 * real0 * imag * imag * imag) + y_c)
        elif power == 7:
            real = (abs(real * real * real * real * real * real * real) -
                    21 * abs(real * real * real * real * real * imag * imag) +
                    35 * abs(real * real * real * imag * imag * imag * imag) -
                    7 * abs(real * imag * imag * imag * imag * imag * imag) + x_c)
            imag = (7 * abs(real0 * real0 * real0 * real0 * real0 * real0 * imag) -
                    35 * abs(real0 * real0 * real0 * real0 * imag * imag * imag) +
                    21 * abs(real0 * real0 * imag * imag * imag * imag * imag) -
                    abs(imag * imag * imag * imag * imag * imag * imag) + y_c)
        elif power == 8:
            real = (real * real * real * real * real * real * real * real +
                    imag * imag * imag * imag * imag * imag * imag * imag -
                    28 * (real * real * real * real * real * real * imag * imag +
                          real * real * imag * imag * imag * imag * imag * imag) +
                    70 * real * real * real * real * imag * imag * imag * imag + x_c)
            imag = (8 * (abs(real0 * real0 * real0 * real0 * real0 * real0 * real0 * imag) -
                         abs(real0 * imag * imag * imag * imag * imag * imag * imag)) +
                    56 * (abs(real0 * real0 * real0 * imag * imag * imag * imag * imag) -
                          abs(real0 * real0 * real0 * real0 * real0 * imag * imag * imag)) + y_c)
        else:
            raise ValueError('Power must be between 2 and 8.')
    return 0


@njit(parallel=True, fastmath=True)
def mandelbrot_julia_set(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon, power=2, mode='mandelbrot'):
    log_horizon = math.log(math.log(horizon))
    r1 = np.linspace(xmin, xmax, length)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((length, height))
    for i in range(length):
        for j in range(height):
            n3[i, j] = mandelbrot_julia(r1[i], r2[j], n, x_c, y_c, log_horizon, horizon, power, mode)
    return r1, r2, n3


@njit(parallel=True, fastmath=True)
def burning_ship_set(xmin, xmax, ymin, ymax, x_c, y_c, height, length, n, horizon, power=2, mode='burning_ship'):
    log_horizon = math.log(math.log(horizon))
    r1 = np.linspace(xmin, xmax, length)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((length, height))
    for i in range(length):
        for j in range(height):
            n3[i, j] = burning_ship(r1[i], r2[j], n, x_c, y_c, log_horizon, horizon, power, mode)
    return r1, r2, n3
