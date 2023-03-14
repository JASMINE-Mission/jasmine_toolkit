import warnings
import erfa
import numpy as np
from astropy.time import Time

from jasmine_toolkit.operation.pointing_freedom import EnumPointingFreedom
from jasmine_toolkit.operation.pointing_mode import EnumPointingMode
from jasmine_toolkit.utils.mapping import Mapping


def test_included_p():
    warnings.simplefilter('ignore', category=erfa.core.ErfaWarning)
    mapping = Mapping(EnumPointingFreedom.POINTING_FIXED, EnumPointingMode.FOUR_FOV_IN_ORBIT,
                      Time('2028-01-01T00:00:00'))
    a = np.array([[0., 0.], [0., 1.], [1., 1.]])
    p = np.array([1.0, 0.0])
    assert mapping.included_p(a, p) == False
    p = np.array([0.1, 0.1])
    assert mapping.included_p(a, p) == True
