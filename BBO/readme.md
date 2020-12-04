# API of BBO

## Optimizer API

All optimization problems are *minimization*.
Lower values of the black-box function are better.

Optimizer submissions should follow this template, for a suggest-observe interface, in your `optimizer.py` :

``` python
from BBO.abstract_optimizer import AbstractOptimizer
from BBO.experiment import experiment_main

class NewOptimizerName(AbstractOptimizer):
    primary_import = None  # Optional, used for tracking the version of optimizer used

    def __init__(self, api_config):
        """Build wrapper class to use optimizer in benchmark.

        Parameters
        ----------
        api_config : dict-like of dict-like
            Configuration of the optimization variables. See API description.
        """
        AbstractOptimizer.__init__(self, api_config)
        # Do whatever other setup is needed
        # ...

    def suggest(self, n_suggestions=1):
        """Get suggestions from the optimizer.

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
        # Do whatever is needed to get the parallel guesses
        # ...
        return next_guess

    def observe(self, X, y):
        """Feed an observation back.

        Parameters
        ----------
        X : list of dict-like
            Places where the objective function has already been evaluated.
            Each suggestion is a dictionary where each key corresponds to a
            parameter being optimized.
        y : array-like, shape (n,)
            Corresponding values where objective has been evaluated
        """
        # Update the model with new objective function observations
        # ...
        # No return statement needed

if __name__ == "__main__":
    # This is the entry point for experiments, so pass the class to experiment_main to use this optimizer.
    # This statement must be included in the wrapper class file:
    experiment_main(NewOptimizerName)
```

You can replace `NewOptimizerName` with the name of your optimizer.

More details on the API can be found [here](https://bayesmark.readthedocs.io/en/latest/readme.html#id1).
Note: do not specify `kwargs` in a `config.json` for the challenge because the online evaluation will not pass any `kwargs` or use the `config.json` .
s

### Configuration space

The search space is defined in the `api_config` dictionary in the constructor to the optimizer (see template above).
For example, if we are optimizing the hyper-parameters for the scikit-learn neural network with ADAM `sklearn.neural_network.MLPClassifier` then we could use the following configuration for `api_config` :

``` python
api_config = \
    {'hidden_layer_sizes': {'type': 'int', 'space': 'linear', 'range': (50, 200)},
     'alpha': {'type': 'real', 'space': 'log', 'range': (1e-5, 1e1)},
     'batch_size': {'type': 'int', 'space': 'linear', 'range': (10, 250)},
     'learning_rate_init': {'type': 'real', 'space': 'log', 'range': (1e-5, 1e-1)},
     'tol': {'type': 'real', 'space': 'log', 'range': (1e-5, 1e-1)},
     'validation_fraction': {'type': 'real', 'space': 'logit', 'range': (0.1, 0.9)},
     'beta_1': {'type': 'real', 'space': 'logit', 'range': (0.5, 0.99)},
     'beta_2': {'type': 'real', 'space': 'logit', 'range': (0.9, 1.0 - 1e-6)},
     'epsilon': {'type': 'real', 'space': 'log', 'range': (1e-9, 1e-6)}}
```

Each key in `api_config` is a variable to optimize and its description is itself a dictionary with the following entries:

* `type` : `{'real', 'int', 'cat', 'bool'}`
* `space` : `{'linear', 'log', 'logit', 'bilog'}`
* `values` : array-like of same data type as `type` to specify a whitelist of guesses
* `range` : `(lower, upper)` tuple to specify a range of allowed guesses

One can also make the following assumption on the configurations:

* `space` will only be specified for types `int` and `real`
* `range` will only be specified for types `int` and `real`
* We will not specify both `range` and `values`
* `bool` does not take anything extra ( `space` , `range` , or `values` )
* The `values` for `cat` will be strings

For `observe` , `X` is a (length `n` ) list of dictionaries with places where the objective function has already been evaluated.
Each suggestion is a dictionary where each key corresponds to a parameter being optimized.
Likewise, `y` is a length `n` list of floats of corresponding objective values.
The observations `y` can take on `inf` values if the objective function crashes, however, it should never be `nan` .

For `suggest` , `n_suggestions` is simply the desired number of parallel suggestions for each guess.
Also, `next_guess` will be a length `n_suggestions` array of dictionaries of guesses, in the same format as `X` .
