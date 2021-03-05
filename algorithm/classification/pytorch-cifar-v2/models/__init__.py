from .nas_models import DARTS_V1, DARTS_V2, AmoebaNet, NASNet
from .preact_resnet import (PreBasic_res_cell_64_2_20,
                            PreBasic_rescell_36_3_20,
                            PreBottleNeck_res_cell_64_2_20,
                            PreBottleNeck_rescell_36_3_20)
from .resnet import (Basic_res_cell, Basic_rescell_36_3_20,
                     BottleNeck_res_cell, BottleNeck_rescell_36_3_20, ResNet18,
                     ResNet34, ResNet50, ResNet101, ResNet152)

model_dict = {
    'darts_v1': DARTS_V1,
    'darts_v2': DARTS_V2,
    'amoebaNet': AmoebaNet,
    'nasnet': NASNet,
    'resnet18': ResNet18,
    'resnet34': ResNet34,
    'resnet50': ResNet50,
    'resnet101': ResNet101,
    'resnet152': ResNet152,
    'basic_resnet_cell': Basic_res_cell,
    'bottleneck_resnet_cell': BottleNeck_res_cell,
    'basic_rescell_36_3_20': Basic_rescell_36_3_20,
    'bottleNeck_rescell_36_3_20': BottleNeck_rescell_36_3_20,
    'PreBasic_res_cell_64_2_20': PreBasic_res_cell_64_2_20,
    'PreBottleNeck_res_cell_64_2_20': PreBottleNeck_res_cell_64_2_20,
    'PreBasic_rescell_36_3_20': PreBasic_rescell_36_3_20,
    'PreBottleNeck_rescell_36_3_20': PreBottleNeck_rescell_36_3_20}


def get_model(model_name):
    return model_dict[model_name]()
