#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' File description '''

from dataclasses import dataclass
from functools import reduce
import numpy as np


__all__ = [
    'PSD_imagesim',
    'coeff_imagesim',
    'ARMAModel',
    'ARIMAModel',
    'ACEModel',
]


def __get_resonance(param):
    ''' Calculate ARMA model coefficients

    Arguments:
        param (array):
            Resonance description. The arary shape should be compatible with
            (N, 2). Each pair contains (amplitude, fractional frequency) pair.

    Returns:
        coefficients of ARMA model
    '''
    param = np.atleast_2d(param)
    if param.shape[1] != 2:
        raise ValueError(
            f'argument "param" has wrong shape ({param.shape})')

    def func(p):
        r, f = p
        if f < 0 or f >= 1:
            raise ValueError(
                f'wrong fractional frequency detected ({f})')
        theta = 2 * np.pi * f
        a = r * np.cos(theta)
        b = r * np.sin(theta)
        return np.array([1, -2 * a, a**2 + b**2])

    return - reduce(np.polymul, [func(p) for p in param])[1:]


def PSD_imagesim(freq):
    freq = np.atleast_1d(freq).reshape((-1, 1))

    f0 = 0.1

    pk = np.array(
        [1e-2, 5e-3, 1.875e-3, 6.25e-4, 1.953e-4, 5.859e-5]).reshape((1, -1))
    hk = np.array(
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]).reshape((1, -1))
    fk = np.array(
        [20, 40, 60, 80, 100, 120]).reshape((1, -1))

    base = f0**2 / (f0**2 + freq**2)
    peak = pk * hk**2 / (hk**2 + (freq - fk)**2)

    return (base + peak.sum(axis=1, keepdims=True)).ravel()


def coeff_imagesim():
    ''' '''
    dt = 5e-4  # 2000 kHz sampling
    f0 = [20, 40, 60, 80, 100, 120]

    A = __get_resonance([[0.999, _ * dt] for _ in f0])
    B = __get_resonance([[0.980, _ * dt] for _ in f0])
    return A, B


@dataclass
class ARMAModel:
    ''' Auto-Regressive and Moving-Average model '''
    ar_coeff: np.ndarray
    ma_coeff: np.ndarray
    sigma: float
    sampling_interval: float = 1.0

    def __post_init__(self):
        self.ar_coeff = np.array(self.ar_coeff)
        self.ma_coeff = np.array(self.ma_coeff)

    def generate(self, n_step, n_warmup=None, seed=None):
        if n_warmup is None:
            n_warmup = np.clip(n_step, min=200, max=1000)

        rng = np.random.default_rng(seed=seed)

        y = np.concatenate([
            np.zeros(n_warmup),
            self.sigma * rng.normal(size=n_step),
        ])
        v = np.concatenate([
            np.zeros(n_warmup),
            self.sigma * rng.normal(size=n_step),
        ])

        def remove_offset(x):
            return x - np.mean(x)

        return remove_offset(self.arma_loop(
            n_warmup, n_step, self.ar_coeff, self.ma_coeff, v, y))

    def psd(self, freq):
        ''' Return the power-spectrum density at frequencies '''
        na = np.arange(1, self.ar_coeff.size + 1).reshape((1, -1))
        nb = np.arange(1, self.ma_coeff.size + 1).reshape((1, -1))
        freq = self.sampling_interval * freq.reshape((-1, 1))

        if na.size > 0:
            dA = 1.0 - np.sum(self.ar_coeff * self.iexp(na * freq), axis=1)
        else:
            dA = np.ones_like(freq).ravel()
        if nb.size > 0:
            dB = 1.0 - np.sum(self.ma_coeff * self.iexp(nb * freq), axis=1)
        else:
            dB = np.ones_like(freq).ravel()

        return self.sigma**2 * np.abs(dB)**2 / np.abs(dA)**2

    @staticmethod
    def iexp(array):
        return np.exp(- 2j * np.pi * array)

    @staticmethod
    def arma_loop(n_warmup, n_sample, A, B, v, y):
        def xdot(x, y):
            return np.sum(np.atleast_1d(x) * np.atleast_1d(y)[::-1])

        for n in range(1, n_warmup + n_sample):
            an = np.max([0, n - A.size])
            bn = np.max([0, n - B.size])
            y[n] = xdot(A[an - n:], y[an:n]) - xdot(B[bn - n:], v[bn:n]) + v[n]
        return y[-n_sample:]


@dataclass
class ARIMAModel(ARMAModel):
    ''' Auto-Regressive Integrated Moving-Average model '''
    depth: int = 1

    def __check_depth(self, depth):
        if depth is None:
            return int(self.depth)
        if (depth < 0):
            raise ValueError(f'depth should be non-negative integer ({depth})')
        else:
            return int(depth)

    def psd(self, freq, depth=None):
        ''' Return the power-spectrum density at fequencies '''
        depth = self.__check_depth(depth)

        if depth == 0:
            return super().psd(freq)
        else:
            norm = (2 * np.pi * freq * self.sampling_interval)**2
            return self.psd(freq, depth=depth - 1) / norm

    def generate(
            self, n_sample, n_warmup=None,
            depth=None, hold=None, seed=None):
        depth = self.__check_depth(depth)

        def remove_offset(x):
            return x - np.mean(x)

        m = hold or n_sample

        if depth == 0:
            return super().generate(
                n_sample, n_warmup=n_warmup, seed=seed)
        else:
            data = self.generate(
                n_sample + m, depth=depth - 1, n_warmup=n_warmup,
                hold=m, seed=seed)
            return remove_offset(np.cumsum(data)[-n_sample:])


@dataclass
class ACEModel(ARMAModel):
    ''' ACE Model by ARMA model '''
    latency: int = 10
    gain: float = 0.0
    target: float = 1.0
    threshold: float = 10.0

    def __post_init__(self):
        if self.latency <= 0:
            raise ValueError(
                f'latency should be positive integer ({self.latency})')
        if self.threshold <= 0:
            raise ValueError(
                f'threshold should be positive float ({self.threshold})')
        if self.target <= 0:
            raise ValueError(
                f'target should be positive float ({self.target})')

        self.arma_loop = \
            self.__generate_ace_loop(
                latency=self.latency,
                gain=self.gain,
                target=self.target,
                threshold=self.threshold,
                interval=self.sampling_interval)

    @property
    def control_interval(self):
        return self.latency * self.sampling_interval

    @property
    def control_frequency(self):
        return 1.0 / self.control_interval

    def psd(self, freq):
        ''' Power Spectral Density Function '''
        raise NotImplementedError(
            'No analytic power spectral density function available')

    @staticmethod
    def __generate_ace_loop(latency, gain, target, threshold, interval):

        def ace_loop(n_warmup, n_sample, A, B, v, y):

            def activate(x):
                return x**3 / (target**2 + x**2)

            def regulate(v, x):
                q = (np.abs(v) - threshold) * np.sign(- v * x)
                return 0.0 if q > 20 else 1.0 / (1.0 + np.exp(q))

            def intervention(n, x, v):
                m = latency * (n // latency)
                mx = np.sum(x[m - latency:m]) / latency
                mv = np.sum(v[m - latency:m]) / latency
                return - gain / latency * activate(mx) * regulate(mv, mx)

            def xdot(x, y):
                return np.sum(x * y[::-1])

            z = np.zeros_like(y)
            for n in range(1, n_warmup + n_sample):
                an = np.max([0, n - A.size])
                bn = np.max([0, n - B.size])
                y[n] = xdot(A[an - n:], y[an:n]) \
                    - xdot(B[bn - n:], v[bn:n]) + v[n]
                y[n] += intervention(n - latency, z, y)
                z[n] = z[n - 1] + y[n] * interval
            return z[-n_sample:]

        return ace_loop
