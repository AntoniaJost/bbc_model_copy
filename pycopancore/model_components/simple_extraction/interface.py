"""model component Interface simple_extraction."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# TODO: use variables from the master data model wherever possible:
# from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """simple extraction"""
    description = "..."
    """A simple extraction model"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:

class Individual(object):
    """Interface for Individual."""

    strategy = Variable('harvesting strategy', 'harvesting strategy indiv.')


class Cell(object):
    """Interface for Cell."""

    stock = Variable('current stock', 'current stock of resource')
    growth_rate = Variable('growth rate', 'growth rate of resource')
