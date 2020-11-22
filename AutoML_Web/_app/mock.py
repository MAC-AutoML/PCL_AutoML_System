import random
USER_LIST=[
	{
		'username':'wuyuhang',
		'tocken':'aighoa[ewfdoBGEh',
		'password':'111111',
		'first_name':'111111',
		'id':1,
	},
	{
		'username':'hello',
		'tocken':'ObFoblKboajw581d',
		'password':'111111',
		'first_name':'111111',
		'id':2,
	},
	{
		'username':'this',
		'tocken':'HognPqkj9896519P',
		'password':'111111',
		'first_name':'111111',
		'id':3,
	},
]

def get_tocken()->str:
	return ''.join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()", 16))