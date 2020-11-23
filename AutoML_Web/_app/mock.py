import random
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

def get_tocken()->str:
	return ''.join(random.sample("0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()", 16))