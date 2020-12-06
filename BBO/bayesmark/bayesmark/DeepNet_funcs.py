from .sklearn_funcs import TestFunction
from algorithm.classification.pytorch_image_classification.configs.
DATASET={"cifar10", "cifar100"}
MODEL_NAME={
"resnet20",
"vgg",
"densenet",
"resnet50",
"resnet110",
}

def DeepNet(TestFunction):
    objective_names = "valid_acc"
    def __init__(self, model_name, dataset, api_config):
        self.model=model_name
        self.dataset=dataset
        self.api_config = api_config

    def evaluation(self, params):
        valid_acc = call_evalute(self.model, self.dataset, params)
        return valid_acc




