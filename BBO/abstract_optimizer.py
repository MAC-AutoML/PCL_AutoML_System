from abc import ABC, abstractmethod


class AbstractOptimizer(ABC):
    """Abstract base class for the optimizers in the benchmark. This creates a common API across all packages.
    """

    # Every implementation package needs to specify this static variable, e.g., "primary_import=opentuner"
    primary_import = None

    def __init__(self, api_config, **kwargs):
        """Build wrapper class to use an optimizer in benchmark.
        Parameters
        ----------
        api_config : dict-like of dict-like
            Configuration of the optimization variables. See API description.
        """
        self.api_config = api_config

    @abstractmethod
    def suggest(self, n_suggestions):
        """Get a suggestion from the optimizer.
        Parameters
        ----------
        n_suggestions : int
            Desired number of parallel suggestions in the output
        Returns
        -------
        next_guess : list of dict
            List of `n_suggestions` suggestions to evaluate the objective
            function. Each suggestion is a dictionary where each key
            corresponds to a parameter being optimized.
        """
        pass

    @abstractmethod
    def observe(self, X, y):
        """Send an observation of a suggestion back to the optimizer.
        Parameters
        ----------
        X : list of dict-like
            Places where the objective function has already been evaluated.
            Each suggestion is a dictionary where each key corresponds to a
            parameter being optimized.
        y : array-like, shape (n,)
            Corresponding values where objective has been evaluated
        """
        pass
