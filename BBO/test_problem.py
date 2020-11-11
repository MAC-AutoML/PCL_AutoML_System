from abc import ABC, abstractmethod


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
