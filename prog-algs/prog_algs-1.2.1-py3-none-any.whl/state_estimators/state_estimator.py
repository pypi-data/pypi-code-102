# Copyright © 2021 United States Government as represented by the Administrator of the National Aeronautics and Space Administration.  All Rights Reserved.

from abc import ABC, abstractmethod, abstractproperty
from ..uncertain_data import UncertainData
from ..exceptions import ProgAlgTypeError
from copy import deepcopy

class StateEstimator(ABC):
    """
    Interface class for state estimators

    Abstract base class for creating state estimators that perform state estimation. Subclasses must implement this interface. Equivilant to "Observers" in NASA's Matlab Prognostics Algorithm Library

    parameters:
     model : ProgModel
        A prognostics model to be used in state estimation
        See: Prognostics Model Package
     x0 : dict
        Initial (starting) state, with keys defined by model.states \n
        e.g., x = {'abc': 332.1, 'def': 221.003} given states = ['abc', 'def']
     measurement_eqn : optional, function
        Measurement equation (x)->z. Usually used in situations where what's measured don't exactly match the output (e.g., different unit, not ever output measured, etc.). see `examples.measurement_eqn_example`
     options : optional, kwargs
        configuration options\n
        Dictionary of any additional configuration values. See state-estimator specific documentation
    """

    default_parameters = {
        't0': 0
    }

    def __init__(self, model, x0, measurement_eqn = None, **kwargs):
        # Check model
        if not hasattr(model, 'output'):
            raise ProgAlgTypeError("model must have `output` method")
        if not hasattr(model, 'next_state'):
            raise ProgAlgTypeError("model must have `next_state` method")
        if not hasattr(model, 'outputs'):
            raise ProgAlgTypeError("model must have `outputs` property")
        if not hasattr(model, 'states'):
            raise ProgAlgTypeError("model must have `states` property")
        self.model = model

        # Check x0
        for key in model.states:
            if key not in x0:
                raise ProgAlgTypeError("x0 missing state `{}`".format(key))
        
        # Check measurement equation
        if measurement_eqn and not callable(measurement_eqn):
            raise ProgAlgTypeError("measurement_eqn must be callable")
        
        # Process kwargs (configuration)
        self.parameters = deepcopy(self.default_parameters)
        self.parameters.update(kwargs)

        self.t = self.parameters['t0']  # Initial Time

    @abstractmethod
    def estimate(self, t, u, z) -> None:
        """
        Perform one state estimation step (i.e., update the state estimate, filt.x)

        Parameters
        ----------
        t : float
            Current timestamp in seconds (≥ 0.0)
            e.g., t = 3.4
        u : dict
            Measured inputs, with keys defined by model.inputs.
            e.g., u = {'i':3.2} given inputs = ['i']
        z : dict
            Measured outputs, with keys defined by model.outputs.
            e.g., z = {'t':12.4, 'v':3.3} given inputs = ['t', 'v']

        Note
        ----
        This method updates the state estimate stored in filt.x, but doesn't return the updated estimate. Call filt.x to get the updated estimate.
        """

    @property
    @abstractproperty
    def x(self) -> UncertainData:
        """
        The current estimated state. 

        Example
        -------
        state = filt.x
        """
