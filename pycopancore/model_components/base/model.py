# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Here the docstring is missing
"""

#
#  Imports
#

from pycopancore import Variable, ODE, Explicit, Step, Event
from .interface import Model_
from pycopancore.model_components import abstract
from . import Cell, Nature, Individual, Culture, Society, Metabolism
import inspect

#
#  Define class Model
#


class Model (Model_, abstract.Model):
    """
    This is the base.model file. It serves two purposes:
    1. Be a the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    #
    # Definitions of class attributes
    #

    entity_types = [Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs
                 ):
        """
        Initializes an instance of Model.

        Parameters
        ----------
        kwargs: dict
            entities being a dict containing entities as entries and their
            class as key
        """

        super().__init__()

        self._process_taxon_objects = {pt: pt() for pt in self.process_taxa}
        self.entities_dict = kwargs['entities']

        # tell all variables, to which entities they belong. Someone should be
        # looking at this code and evaluate if this is sane...
        # First iterate throug all variables:
        for (v, oc) in self.variables:
            # iterate through the dictionary
            for key, item in self.entities_dict.items():
                # iterate through subclasses of owning class, since when a
                # class is used in more than one study, the right study has to
                # be chosen:
                for subclass in oc.__subclasses__():
                    if subclass == key:
                        v.entities = item
                        continue

        # TODO:
        # is it necessary to make all items in self.entities_dict known
        # to the object itself? Then we need something like this:
        #   for et in Model.entity_types:
        #       for key, item in self.entities_dict.items():
        #           for subclass in et.__subclass__():
        #               if subclass == key:
        #                   self.('et'+'s') = item
        #
        # This is doing something like this hopefully:
        # subclass = find the right subclass (study)
        # self.cells = entities[subclass]
        # But how do I tell it, that the variable is e.g. cells and not 'Cells'

        print('     base model instantiated')

    def __repr__(self):
        """
        Return a string representation of the object of class base.Model.
        """
        # Is it necessary to list all objects? Or are classes sufficient?
        keys_entities = []
        keys_process_taxa = []
        for key, item in self.entities_dict:
            keys_entities.append(key)
        for key, item in self._process_taxon_objects:
            keys_process_taxa.append(key)
        return (super().__repr__() +
                ('base.model object with entities %r /'
                 'and process taxa %r'
                 ) % (keys_entities,
                      keys_process_taxa
                      )
                )

    #
    #  Definitions of further methods
    #

    @property
    def entities(self):
        """
        A function to return a dictionary with classes as key and entities as
        entries

        Returns
        -------
        A dictionary with classes as key and entites as entries
        """
        # Is it better to have the owning class as key or the subclass, so
        # for example base.Cell or base_and_dummy.Cell?

        entities_dict_2 = {}
        for key, item in self.entities_dict.items():
            print('\n key', key)
            print('\n items:', item)

        return self.entities_dict

    @classmethod
    def configure(cls):
        """
        This classmethod configures the mixin models by allocating variables
        and processes to designated lists.
        """

        cls.entity_variables = []
        cls.taxon_variables = []

        cls.variables = []  # save in pairs: (variable, owning_class)
        cls.processes = []  # save in pairs: (process, owning_class)

        cls.variables_dict = {}

        cls.ODE_variables = []
        cls.explicit_variables = []
        cls.step_variables = []
        cls.event_variables = []

        cls.ODE_processes = []
        cls.explicit_processes = []
        cls.step_processes = []
        cls.event_processes = []

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not abstract.Model
                          and abstract.Model in inspect.getmro(c)
                          ]
        print('components are:', cls.components)
        for c in cls.components:
            interfaceclass = c.__bases__[0]
            print("Model component:", interfaceclass.name, "(", c, ")...")
            # Iterate through all mixins of the component:
            for et in c.entity_types:
                print('     entity-type', et)
                cparents = list(inspect.getmro(et))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("         variable:", v)
                    # check if same var. object was already registered:
                    if v in [v2 for (v2, et2) in cls.variables]:
                        print("already registered by another component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict:
                        print("already registered by another component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v
                    cls.variables.append((v, et))

                for p in et.processes:
                    print("         process:", p)
                    cls.processes.append((p, et))

            # Iterate through all process taxon mixins:
            for pt in c.process_taxa:
                print('     process taxon', pt)
                cparents = list(inspect.getmro(pt))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("         variable:", v)
                    # check if same var. object was already registered:
                    if v in [v2 for (v2, et2) in cls.variables]:
                        print("already registered by another component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict:
                        print("already registered by another component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v
                    cls.variables.append((v, pt))

                for p in pt.processes:
                    print("         process:", p)
                    cls.processes.append((p, pt))

            for (process, owning_class) in cls.processes:
                if isinstance(process, ODE):
                    cls.ODE_variables += [(v, owning_class)
                                          for v in process.variables]
                    cls.ODE_processes += [(process, owning_class)]
                elif isinstance(process, Explicit):
                    cls.explicit_variables += [(v, owning_class)
                                               for v in process.variables]
                    cls.explicit_processes += [(process, owning_class)]
                elif isinstance(process, Step):
                    cls.step_variables += [(v, owning_class)
                                           for v in process.variables]
                    cls.step_processes += [(process, owning_class)]
                elif isinstance(process, Event):
                    cls.event_variables += [(v, owning_class)
                                            for v in process.variables]
                    cls.event_processes += [(process, owning_class)]
                else:
                    print('process-type of', process, 'not specified')
                    print(process.__class__.__name__)
                    print(object.__str__(process))
            # TODO: Why is python always appending 2 processes?

        print("...done")
