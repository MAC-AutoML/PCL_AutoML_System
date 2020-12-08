'''
read the result from the log
'''
import os
from datetime import datetime


if __name__ == "__main__":
    experiment_path = os.path.abspath('./experiments')
    model_list = os.listdir(experiment_path)
    model_list.sort()
    for model in model_list:
        md_str = '|'
        if len(model) > 5:
            md_str += model[0:-28]
            # _list = model.split('_')
            # if _list[0] == 'darts':
            #     md_str += _list[0] + '_' + _list[1]
            # else:
            #     md_str += _list[0]
            md_str += "|"
            model_log_path = os.path.join(experiment_path, model, 'logger.log')
            if os.path.isfile(model_log_path):
                with open(model_log_path) as f:
                    log_lines = f.readlines()
                start_time = datetime.strptime(
                    log_lines[0][0:17], '%m/%d %I:%M:%S %p')
                end_time = datetime.strptime(
                    log_lines[-1][0:17], '%m/%d %I:%M:%S %p')
                training_hours = (end_time - start_time).total_seconds() / \
                    3600.
                for line in log_lines:
                    if 'Model size' in line:
                        model_size = line.split('=')[-1][0:-1]
                    if 'FLOPs' in line:
                        flops = line.split('=')[-1][0:-1]
                md_str += log_lines[-1].split('=')[-1][0:-1]
                md_str += '|'
                md_str += model_size
                md_str += '|'
                md_str += flops
                md_str += '|'
                md_str = md_str + str(training_hours) + '|'
                md_str = md_str + \
                    log_lines[2].split('=')[-1][0:-1] + '             |'
                md_str = md_str + log_lines[7].split('=')[-1][0:-1] + '      |'
                md_str = md_str + log_lines[4].split('=')[-1][0:-1] + '    |'
                print(md_str)
                # print("Hyper-parameters is:")
                # print(log_lines[2])
                # print(log_lines[4])
                # print(log_lines[7])

                # print(log_lines[-1])
