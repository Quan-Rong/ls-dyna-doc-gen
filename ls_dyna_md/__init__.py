__version__ = "1.1.0"
__author__ = "Antigravity Agent"
__description__ = "LS-Dyna Documentation Generator"

from .parser import LSDynaParser
from .writers.detailed_writer import DetailedWriter
from .writers.overview_writer import OverviewWriter
