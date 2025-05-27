#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Test cases for trajectory module '''

from pytest import fixture
import numpy as np

from ..trajectory import Trajectory, FFTTrajectory


@fixture
def canvas():
    ''' Fixture to create a canvas for testing '''
    return np.zeros((255, 255))


def test_trajectory_init(canvas):
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    traj = Trajectory(x, y, canvas_size=127)

    assert isinstance(traj, Trajectory)
    assert traj.canvas_size == 127
    assert np.array_equal(traj.x, x)
    assert np.array_equal(traj.y, y)
    assert traj.canvas.shape == (127, 127)
    assert traj.extent == [-63.5, 63.5, -63.5, 63.5]
    assert traj.fft_canvas.shape == (127, 127)
    assert traj.convolve(canvas).shape == (255, 255)


def test_ffttrajectory_init(canvas):
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 2])
    traj = FFTTrajectory(x, y, canvas_size=127)

    assert isinstance(traj, FFTTrajectory)
    assert traj.canvas_size == 127
    assert np.array_equal(traj.x, x)
    assert np.array_equal(traj.y, y)
    assert traj.canvas.shape == (127, 127)
    assert traj.extent == [-63.5, 63.5, -63.5, 63.5]
    assert traj.fft_canvas.shape == (127, 127)
    assert traj.convolve(canvas).shape == (255, 255)
