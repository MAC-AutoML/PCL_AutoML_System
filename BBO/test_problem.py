from abc import ABC, abstractmethod
import numpy as np


class TestFunction(ABC):
    """Abstract base class for test functions in the benchmark. These do not need to be ML hyper-parameter tuning.
    """

    def __init__(self):
        """Setup general test function for benchmark. We assume the test function knows the meta-data about the search
        space, but is also stateless to fit modeling assumptions. To keep stateless, it does not do things like count
        the number of function evaluations.
        """
        # This will need to be set before using other routines
        self.api_config = None

    @abstractmethod
    def evaluate(self, params):
        """Abstract method to evaluate the function at a parameter setting.
        """

    def get_api_config(self):
        """Get the API config for this test problem.

        Returns
        -------
        api_config : dict(str, dict(str, object))
            The API config for the used model. See README for API description.
        """
        assert self.api_config is not None, "API config is not set."
        return self.api_config

class rastrigin_function(TestFunction):
    def __init__(self):
        self.api_config ={
           "x1": {"type": "real", "space": "linear", "range": (-5.12, 5.12)},
           "x2": {"type": "real", "space": "linear", "range": (-5.12, 5.12)},
        }

    def evaluate(self, params):
        print(params)
        f_x = 10. * len(params)
        for key, value in params.items():
            # print('key', key)
            # print('value', value)
            f_x += value ** 2 - 10 * np.cos(2 * np.pi * value)
        return f_x