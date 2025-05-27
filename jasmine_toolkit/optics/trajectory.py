#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Trajectory of 2D jitter motion'''

from scipy.signal import convolve

import numpy as np
import scipy.fft as fft


__all__ = [
    'Trajectory',
    'FFTTrajectory',
]


class Trajectory:
    ''' Trajectory: Container of 2D jitter motion.

    The class handles a 2D jitter motion and generates a convolution kernel for
    the trajectory. It takes a list of x and y coordinates.

    Attributes:
        canvas (ndarray):
            A copy of the canvas with the trajectory applied
        canvas_size (int):
            The size of the square canvas
        fft_canvas (ndarray):
            The 2D Fourier transform of the canvas
        extent (list):
            The extent of the canvas in terms of the x and y axes
        x (ndarray):
            A copy of the x-coordinates of the trajectory
        y (ndarray):
            A copy of the y-coordinates of the trajectory
        ix (ndarray):
            The integer part of the x-coordinates
        iy (ndarray):
            The integer part of the y-coordinates
        dx (ndarray):
            The fractional part of the x-coordinates
        dy (ndarray):
            The fractional part of the y-coordinates
    '''

    def __init__(self, x, y, canvas_size=255):
        ''' Generate a trace instance

        Arguments:
            x (ndarray):
                The x-coordinates of jitter motion
            y (ndarray):
                The y-coordinates of jitter motion

        Options:
            canvas_size (int):
                The size of the square canvas. Must be an odd number
        '''
        assert canvas_size % 2 == 1
        self.__x = np.atleast_1d(x).reshape((-1, ))
        self.__y = np.atleast_1d(y).reshape((-1, ))
        self.__canvas_size = canvas_size
        self.__canvas = np.zeros((self.canvas_size, self.canvas_size))

        for ix, iy, dx, dy in self.__get_trace:
            ix = ix + (self.canvas_size // 2) + 1
            iy = iy + (self.canvas_size // 2) + 1
            self.__canvas[iy - 2:iy + 1, ix - 2:ix + 1] += self.__patch(dx, dy)

    @property
    def canvas_size(self):
        ''' The size of the canvas '''
        return self.__canvas_size

    @property
    def canvas(self):
        ''' The canvas with the jitter trajectory '''
        return self.__canvas.copy()

    @property
    def fft_canvas(self):
        ''' The 2D Fourier transform of the canvas '''
        return fft.fft2(self.__canvas)

    @property
    def extent(self):
        return [
            - (self.canvas_size // 2) - 0.5,
            + (self.canvas_size // 2) + 0.5] * 2

    @property
    def x(self):
        return self.__x.copy()

    @property
    def y(self):
        return self.__y.copy()

    @property
    def ix(self):
        return np.floor(self.x + 0.5).astype('int32')

    @property
    def iy(self):
        return np.floor(self.y + 0.5).astype('int32')

    @property
    def dx(self):
        return self.x - self.ix

    @property
    def dy(self):
        return self.y - self.iy

    @staticmethod
    def _weight(dx):
        return np.clip(1 - np.abs(dx), min=0)

    @property
    def __get_trace(self):
        return zip(self.ix, self.iy, self.dx, self.dy)

    def __patch(self, dx, dy):
        assert (-0.5 <= dx) & (dx <= 0.5)
        assert (-0.5 <= dy) & (dy <= 0.5)
        ix = np.array([-1, 0, 1]).reshape((1, -1))
        iy = np.array([-1, 0, 1]).reshape((-1, 1))
        wx = self._weight(dx - ix)
        wy = self._weight(dy - iy)
        return wx * wy

    def convolve(self, image):
        ''' Convolve the image with the trajectory canvas '''
        return convolve(image, self.canvas, mode='same')


class FFTTrajectory(Trajectory):
    ''' FFTTrajectory: Container of 2D jitter motion.

    The class directly generates a convolution kernel for the trajectory in
    the Fourier domain. This class is implemented just for curiosity. The
    performance is not better than the Trajectory class.

    Attributes:
        canvas (ndarray):
            A copy of the canvas with the trajectory applied
        canvas_size (int):
            The size of the square canvas
        fft_canvas (ndarray):
            The 2D Fourier transform of the canvas
        extent (list):
            The extent of the canvas in terms of the x and y axes
        x (ndarray):
            A copy of the x-coordinates of the trajectory
        y (ndarray):
            A copy of the y-coordinates of the trajectory
        ix (ndarray):
            The integer part of the x-coordinates
        iy (ndarray):
            The integer part of the y-coordinates
        dx (ndarray):
            The fractional part of the x-coordinates
        dy (ndarray):
            The fractional part of the y-coordinates
    '''
    def __init__(self, x, y, canvas_size=255):
        super().__init__(x, y, canvas_size=canvas_size)
        self.__x = np.atleast_1d(x).reshape((-1, ))
        self.__y = np.atleast_1d(y).reshape((-1, ))

        self.__fft_canvas = np.zeros(
            (canvas_size, canvas_size), dtype='complex')
        for _x, _y in zip(self.__x, self.__y):
            self.__fft_canvas += self.__plane(_x, _y)

    @property
    def canvas(self):
        return np.real(fft.ifft2(self.__fft_canvas))

    @property
    def fft_canvas(self):
        return self.__fft_canvas.copy()

    @property
    def kernel(self):
        return self.__kernel.copy()

    @property
    def __axis(self):
        return np.arange(0, self.canvas_size)

    @property
    def ax(self):
        return self.__axis.reshape((1, -1)) / self.canvas_size

    @property
    def ay(self):
        return self.__axis.reshape((-1, 1)) / self.canvas_size

    def __eax(self, ix):
        sx = ix + (self.canvas_size // 2)
        return np.exp(- 2 * np.pi * 1J * sx * self.ax)

    def __eay(self, iy):
        sy = iy + (self.canvas_size // 2)
        return np.exp(- 2 * np.pi * 1J * sy * self.ay)

    def __patch(self, dx, dy):
        raise NotImplementedError(
            'FFTTrajectory does not support __patch method')

    def __plane(self, x, y):
        ix = np.floor(x + 0.5).astype('int32')
        iy = np.floor(y + 0.5).astype('int32')
        wx = self._weight(np.array([-1, 0, 1]) - (x - ix))
        wy = self._weight(np.array([-1, 0, 1]) - (y - iy))

        eax = wx[0] * self.__eax(ix - 1) \
            + wx[1] * self.__eax(ix) + wx[2] * self.__eax(ix + 1)
        eay = wy[0] * self.__eay(iy - 1) \
            + wy[1] * self.__eay(iy) + wy[2] * self.__eay(iy + 1)
        return eax * eay
