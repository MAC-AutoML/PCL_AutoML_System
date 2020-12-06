import random
import datetime
import time
from typing import List

from random_words import RandomNicknames
rn = RandomNicknames()
# string for random.sample()
LOWER_LETTER='qwertyuiopasdfghjklzxcvbnm'
UPPER_LETTER='QWERTYUIOPASDFGHJKLZXCVBNM'
LETTER=LOWER_LETTER+UPPER_LETTER
NUMBER='1234567890'
SAFE_CASE='_-'
OTHER_CASE='!@#$%^&*()[];:,'

USER_LIST=[
	{
		'username':'wuyuhang',
		'tocken':'$^%2l&)6yn0p@xfs',
		'password':'111111',
		'first_name':'wuyuhang',
		'id':1,
	},
	{
		'username':'hello',
		'tocken':'ObFoblKboajw581d',
		'password':'111111',
		'first_name':'he',
		'id':2,
	},
	{
		'username':'this',
		'tocken':'HognPqkj9896519P',
		'password':'111111',
		'first_name':'thi',
		'id':3,
	},
]
DATASET_LIST=[
	{
		# 'name':'ImageNet 2012',
		# 'path':'/src/data/imagenet',
		'label':'ImageNet 2012',
		'value':'/src/data/imagenet',
	},
	{
		# 'name':'cifar 10',
		# 'path':'/src/data/cifar10',
		'label':'cifar 10',
		'value':'/src/data/cifar10',
		
	},
	{
		# 'name':'kinetics',
		# 'path':'/src/data/kinetics',
		'label':'kinetics',
		'value':'/src/data/kinetics',
		
	},
]
def get_tocken()->str:
	return ''.join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()", 16))
	
def get_fake_time()->str:
    ## 这里最后的毫秒数有六位，antd前端时间毫秒数只有三位
    rand_time=datetime.datetime.now()-datetime.timedelta(\
				days	=random.randint(0,7), \
				hours	=random.randint(0,24), \
				minutes	=random.randint(0,60))
    rand_time=rand_time.strftime('%Y-%m-%dT%H:%M:%S.')
    return rand_time+''.join(random.sample("123456789",3))+'Z'

def get_fake_dir(length:int=5)->str:
    return ''.join(random.sample(LETTER,length))+'/'

def get_fake_file(length:int=8)->str:
    head=2
    fake_file = ''.join(random.sample(LETTER,head))+\
				''.join(random.sample(LETTER+NUMBER+SAFE_CASE,length-head))+'.'+\
        		''.join(random.sample(LOWER_LETTER,3))
        
def get_fake_path(levels:int=4)->str:
    root='/'
    for i in range(levels):
        root=root+get_fake_dir()
    return root
def get_fake_title(length:int=5)->str:
    
    name=rn.random_nick(gender='u')
    index=''.join(random.sample(NUMBER,length))
    return name+'_'+index
## generate test data for AutoML mission
m_type=['image_classifica','object_detection','predict_analysis']
train_s=['wait','run','stop','success','error']
deploy_s=['single','multiple','error','wait']

def genAutoItem(i:int)->dict:
    return {
	'id':random.randint(1,1e4),
	'title':get_fake_title(),
	'type':m_type[random.randint(0,len(m_type)-1)],
	'train_status':train_s[random.randint(0,len(train_s)-1)],
	'deploy_status':deploy_s[random.randint(0,len(deploy_s)-1)],
	'data_source':get_fake_path(4),
	'created_at':get_fake_time()
	}
def genAutoList(num:int=10)->list:
    result=[ genAutoItem(i) for i in range(num)]
    return result
## generate test data for 

FAKE_Automl=genAutoList(20)


if(__name__=="__main__"):
    # print(get_time())
    # a=datetime.datetime.now()
    # b=datetime.datetime.now()-datetime.timedelta(\
    #         days	=random.randint(0,7), \
	# 		hours	=random.randint(0,24), \
    #    		minutes	=random.randint(0,60))
    # print(a)
    # print(b)
    [print(i) for i in genAutoList(2)]

    
