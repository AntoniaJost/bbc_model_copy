"""Culture process taxon mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Culture.individuals:
#from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit, Event
import numpy as np
class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    processes = [
                 ]

