algo_creater = {
    'name':
    'kkTestNet',
    'resource':
    1,
    'hyperDict': [{
        'id': 2,
        'name': 'lr',
        'dataType': 'int',
        'default': '0.1',
        'necessray': True
    }, {
        'id': 1626434479146,
        'name': '32',
        'dataType': 'float',
        'default': 's'
    }],
    'ioDict': [{
        'id': 2,
        'label': 'out',
        'name': 'output',
        'path': 'user01/'
    }, {
        'id': 1626434497414,
        'label': 'd',
        'name': 'df',
        'path': 'dfg'
    }]
}
job_response = {
    'code': 'S000',
    'msg': 'success',
    'payload': {
        'id': 'bd993f300e779011eb0891304939b5259323',
        'name': 'test_job301',
        'platform': 'k8s',
        'jobStatus': {
            'username': 'wuyh',
            'state': 'SUCCEEDED',
            'subState': 'SUCCEEDED',
            'executionType': 'START',
            'retries': 0,
            'createdTime': 1626579683000,
            'completedTime': 1626579693000,
            'appId': '691ac20a-d421-43f8-b74d-f3315d95f037',
            'appProgress': '',
            'appTrackingUrl': '',
            'appLaunchedTime': 1626579683000,
            'appCompletedTime': 1626579693000,
            'appExitCode': 0,
            'appExitDiagnostics': {
                "podRoleName": {
                    "main-0": "main-0"
                },
                "podEvents": {
                    "main-0": [{
                        "uid": "14cbcf2a-fd10-486f-8ba0-917fdbf1a078",
                        "reason": "Scheduled",
                        "message":
                        "Successfully assigned 472e103b6e7c21d639354fe5abfa80a8/bd993f300e779011eb0891304939b5259323-main-0 to agx-17",
                        "reportingController": "",
                        "action": ""
                    }, {
                        "uid": "50f35216-1996-49e1-9a6f-23e92706b9e0",
                        "reason": "Pulled",
                        "message":
                        "Container image \"dockerhub.pcl.ac.cn:5000/user-images/wuyh:base\" already present on machine",
                        "reportingController": "",
                        "action": ""
                    }, {
                        "uid": "251452e7-ded1-4d8b-88ff-d277acbc2f99",
                        "reason": "Created",
                        "message": "Created container main-container",
                        "reportingController": "",
                        "action": ""
                    }, {
                        "uid": "9d50e8a5-c1c2-4fe8-b1da-4625d012b336",
                        "reason": "Started",
                        "message": "Started container main-container",
                        "reportingController": "",
                        "action": ""
                    }]
                },
                "extras": []
            },
            'appExitType': None,
            'virtualCluster': 'pcl-yunnao'
        },
        'taskRoles': {
            'main': {
                'taskRoleStatus': {
                    'name': 'main'
                },
                'taskStatuses': [{
                    'taskIndex': 0,
                    'podUid': 'e9de5d83-f1e4-4f96-8806-259287826929',
                    'podIp': '10.211.168.50',
                    'podName': 'bd993f300e779011eb0891304939b5259323-main-0',
                    'containerId':
                    'ea1960cab66a28fb4598b0dd8fcb401259e7e24a5b5cb4a00ba31178398a4b20',
                    'containerIp': '192.168.202.137',
                    'containerGpus': '',
                    'state': 'SUCCEEDED',
                    'startAt': '2021-07-18T03:41:18Z',
                    'finishedAt': '2021-07-18T03:41:32Z',
                    'exitCode': 0,
                    'exitDiagnostics': '',
                    'retriedCount': 0
                }]
            }
        },
        'resource': {
            'cpu': 4,
            'memory': '32768Mi',
            'nvidia.com/gpu': 1
        },
        'config': {
            'image':
            'dockerhub.pcl.ac.cn:5000/user-images/wuyh:base',
            'jobId':
            'bd993f300e779011eb0891304939b5259323',
            'gpuType':
            'dgx',
            'jobName':
            'test_job301',
            'jobType':
            'dgx',
            'isPreempt':
            False,
            'taskRoles': [{
                'name': 'main',
                'shmMB': 16384,
                'useNNI': False,
                'command':
                'cd /userhome/ && python test.py --epoch 205 --lr 0.13 --output ./result.txt',
                'memoryMB': 32768,
                'cpuNumber': 4,
                'gpuNumber': 1,
                'mluNumber': 0,
                'fpgaNumber': 0,
                'isMainRole': False,
                'taskNumber': 1,
                'needIBDevice': False,
                'minFailedTaskCount': 1,
                'minSucceededTaskCount': 1
            }],
            'retryCount':
            0,
            'typeAction':
            'no_debug',
            'priorityClass':
            'init'
        },
        'userinfo': {
            'user': '472e103b6e7c21d639354fe5abfa80a8',
            'org_id': ''
        }
    }
}
get_jobInfo = {
    'code': 'S000',
    'msg': 'success',
    'payload': {
        'id': 'dd22b2700e9cc011eb0918702bd7ddedd51c',
        'name': 'kktestnet2',
        'platform': 'k8s',
        'jobStatus': {
            'username': 'wuyh',
            'state': 'WAITING',
            'subState': 'WAITING',
            'executionType': 'START',
            'retries': 0,
            'createdTime': 0,
            'completedTime': 1626834816943,
            'appId': '63814f62-0ca8-450b-bbfb-0d2ee93b0fa7',
            'appProgress': '',
            'appTrackingUrl': '',
            'appLaunchedTime': 0,
            'appCompletedTime': '',
            'appExitCode': 0,
            'appExitDiagnostics': '[]',
            'appExitType': None,
            'virtualCluster': 'pcl-yunnao'
        },
        'taskRoles': {
            'main': {
                'taskRoleStatus': {
                    'name': 'main'
                },
                'taskStatuses': [{
                    'taskIndex': 0,
                    'podUid': '',
                    'podIp': '',
                    'podName': 'dd22b2700e9cc011eb0918702bd7ddedd51c-main-0',
                    'containerId': None,
                    'containerIp': '',
                    'containerGpus': '',
                    'state': 'WAITING',
                    'startAt': None,
                    'finishedAt': None,
                    'exitCode': 0,
                    'exitDiagnostics': '',
                    'retriedCount': 0
                }]
            }
        },
        'resource': {
            'cpu': 4,
            'memory': '16384Mi',
            'nvidia.com/gpu': 0
        },
        'config': {
            'image':
            'dockerhub.pcl.ac.cn:5000/user-images/wuyh:base',
            'jobId':
            'dd22b2700e9cc011eb0918702bd7ddedd51c',
            'gpuType':
            'dgx',
            'jobName':
            'kktestnet2',
            'jobType':
            'dgx',
            'isPreempt':
            False,
            'taskRoles': [{
                'name': 'main',
                'shmMB': 8192,
                'useNNI': False,
                'command':
                'cd /userhome/ && python test.py --epoch 200 --lr 0.15 --output hooker/result.txt',
                'memoryMB': 16384,
                'cpuNumber': 4,
                'gpuNumber': 0,
                'mluNumber': 0,
                'fpgaNumber': 0,
                'isMainRole': False,
                'taskNumber': 1,
                'needIBDevice': False,
                'minFailedTaskCount': 1,
                'minSucceededTaskCount': 1
            }],
            'retryCount':
            0,
            'typeAction':
            'no_debug',
            'priorityClass':
            'init'
        },
        'userinfo': {
            'user': '472e103b6e7c21d639354fe5abfa80a8',
            'org_id': ''
        }
    }
}
autoSearch_return_dict = {
    'name':
    'Piop',
    'method':
    'BORE',
    'epoch':
    1,
    'suggest':
    2,
    'result':
    '/hooker/k/Result.txt',
    'resource':
    1,
    'algo': {
        'id':
        2,
        'hyperDict': [{
            'id': 5,
            'name': 'waremp',
            'dataType': 'int',
            'default': '122',
            'necessray': False
        }],
        'ioDict': [{
            'id': 3,
            'label': 'output',
            'name': 'outpath',
            'path': 'hooker/k/'
        }, {
            'id': 2,
            'label': 'datapath',
            'name': 'datapath',
            'path': 'cifar/'
        }, {
            'id': 1626961537341,
            'label': 'timelog',
            'name': 'log',
            'path': 'user01/data/'
        }]
    },
    'search_para': [{
        'id': 4,
        'name': 'epoch',
        'dataType': 'int',
        'default': '231',
        'necessray': False,
        'index': 1,
        'searchType': 'range',
        'space': 'log',
        'content': '12 200'
    }]
}
aut2 = {
    'name':
    'tt',
    'method':
    'HyperBand',
    'epoch':
    12,
    'suggest':
    4,
    'result':
    '/userhome/hes/result.txt',
    'resource':
    1,
    'algo': {
        'id':
        2,
        'hyperDict': [{
            'id': 5,
            'name': 'waremp',
            'dataType': 'int',
            'default': '122',
            'necessray': False
        }, {
            'id': 4,
            'name': 'epoch',
            'dataType': 'int',
            'default': '230',
            'necessray': False
        }],
        'ioDict': [{
            'id': 3,
            'label': 'output',
            'name': 'outpath',
            'path': 'user01/'
        }, {
            'id': 2,
            'label': 'datapath',
            'name': 'datapath',
            'path': 'hooker/'
        }]
    },
    'search_para': [{
        'id': 3,
        'name': 'learning_rate',
        'dataType': 'float',
        'default': '0.3',
        'necessray': True,
        'index': 2,
        'searchType': 'range',
        'space': 'linear',
        'content': '1 3'
    }]
}
auto3 = {
    'name':
        'trys',
    'method':
        'BBO',
    'epoch':
        15,
    'suggest':
        5,
    'result':
        '/tttt',
    'resource':
        1,
    'algo': {
        'id':
        2,
        'hyperDict': [{
            'id': 4,
            'name': 'epoch',
            'dataType': 'int',
            'default': '231',
            'necessray': False
            }, {
            'id': 3,
            'name': 'learning_rate',
            'dataType': 'float',
            'default': '0.3',
            'necessray': True
        }],
        'ioDict': [{
            'id': 3,
            'label': 'output',
            'name': 'outpath',
            'path': 'hooker/'
            }, {
            'id': 2,
            'label': 'datapath',
            'name': 'datapath',
            'path': 'user01/'
        }]
    },
    'search_para': [{
        'id': 5,
        'name': 'waremp',
        'dataType': 'int',
        'default': '122',
        'necessray': False,
        'index': 0,
        'searchType': 'values',
        'space': 'logit',
        'content': '1 2 3 4 5 6 7'
    }]
}
