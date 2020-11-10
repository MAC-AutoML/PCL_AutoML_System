from torchvision.models import vgg16
from thop import profile
from thop import clever_format
from pytorch_image_classification.models import *
from train import load_config
config = load_config()
model = create_model(config)
input = torch.randn(1, 3, 224, 224)
#flops, params = profile(model,inputs=(input, ))
#print(flops, params)
flops, params = clever_format([12508275712.0,1730714.0])
print(flops, params) #resnet110 12.508G 1.731M
flops, params = clever_format([6215001088.0,855770.0], "%.3f")
print(flops, params) #resnet56 6.215G 855.770K
flops, params = clever_format([14527502336.0,769162.0], "%.3f")
print(flops, params) #densenet 14.528G 769.162K
flops, params = clever_format([2019484928.0,272474.0], "%.3f")
print(flops, params) # resnet20 2.019G 272.474K
flops, params = clever_format([15607495680.0,138357536.0], "%.3f")
print(flops, params) #vgg16 15.607G 138.358M
#resnet110 12508275712.0,1730714.0
#resnet56 6215001088.0,855770.0
#densenet 14527502336.0,769162.0
#resnet20 2019484928.0,272474.0
#vgg16 15607495680.0,138357536.0