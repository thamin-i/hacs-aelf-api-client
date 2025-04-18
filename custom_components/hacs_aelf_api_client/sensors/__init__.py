"""List all sensors so that they can be easily imported"""

from .complines import ComplinesSensor
from .lauds import LaudsSensor
from .masses import MassesSensor
from .none import NoneSensor
from .readings import ReadingsSensor
from .sext import SextSensor
from .terce import TerceSensor
from .vespers import VespersSensor

__all__ = [
    "ComplinesSensor",
    "LaudsSensor",
    "MassesSensor",
    "NoneSensor",
    "ReadingsSensor",
    "SextSensor",
    "TerceSensor",
    "VespersSensor",
]
