from abc import ABC, abstractmethod
import numpy as np
import os
from tools import API_tools

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
    def evaluate(self, params,ii,jj):
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
    def __init__(self,algpath,ouputdir):
        self.api_config ={
           "x1": {"type": "real", "space": "linear", "range": (-5.12, 5.12)},
           "x2": {"type": "real", "space": "linear", "range": (-5.12, 5.12)},
        }
        self.ouputdir = ouputdir
        self.algpath = algpath

    def printinfo(self):
        return self.ouputdir,self.algpath

    def evaluate(self, params,ii,jj):
        print(params["x1"])
        f_x = 10. * len(params)
        for key, value in params.items():
            # print('key', key)
            # print('value', value)
            f_x += value ** 2 - 10 * np.cos(2 * np.pi * value)
        return f_x


class classify_train(TestFunction):
    def __init__(self,algpath,ouputdir):
        self.api_config ={
           "lr": {"type": "real", "space": "linear", "range": (0.0001, 0.1)},
           "momentum": {"type": "real", "space": "linear", "range": (0.9, 0.99)},
           "weight_decay": {"type": "real", "space": "linear", "range": (1e-5, 3e-4)},
        }
        self.ouputdir = ouputdir
        self.algpath = algpath

    def printinfo(self):
        return self.ouputdir,self.algpath

    def evaluate(self, params,ii,jj):
        print(params)
        new_outpath = self.ouputdir + "/bbo_out_" + str(ii) + "_" + str(jj)
        if os.path.exists(self.ouputdir) != True:
            os.makedirs(self.ouputdir)
        if os.path.exists(new_outpath) != True:
            os.makedirs(new_outpath)
        command = "cd " + self.algpath[0:-8] + ";PYTHONPATH=./ python train.py --lr " + str(params["lr"]) + " --outputdir " + str(new_outpath)
        print(str("bbo_"+str(ii)+"_"+str(jj)),command)
        info = API_tools.creat_mission(str("bbo_"+str(ii)+"_"+str(jj)), command, "qwer", "wudch", "woodchen")
        return True