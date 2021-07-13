#
## AutoML_Web/backend/hyperp_save_test.py

import yaml

d = {'a':1, 0:2, 'sd':{0:1,2:{3:1}}}
fp = open('../HyperP_Save/dict_debug.yaml', 'w')
fp.write(yaml.dump(d))
fp.close()

import yaml

fp = open('../HyperP_Save/dict_debug.yaml', 'r')
st = fp.read()
fp.close()

dd = yaml.load(st,Loader=yaml.FullLoader)
print(dd)