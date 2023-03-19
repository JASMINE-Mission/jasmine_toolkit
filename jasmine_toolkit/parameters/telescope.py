#!/usr/bin/env python
from .parameter import Parameter

__all__ = (
    'effective_focal_length',
)

effective_focal_length = Parameter(
    'effective_focal_length',
    3776.0,
    'mm',
    '',
    'default value')
