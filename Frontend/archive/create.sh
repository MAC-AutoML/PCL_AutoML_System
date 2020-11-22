#!/bin/bash

filelist=(
    OverView
    AutoML
    DataManage
    DevEnv
    AlgoManage
    JobManage
    ModelManage
    AIMarket
)
for item in ${filelist[@]}
do
    mkdir "$item"
    touch "$item/index.tsx"
    touch "$item/index.less"
done

# for model in ${Model_list[@]} 
#     do
#         echo "MODEL IS : $model"
#         bash scripts/batch_train.sh $model
#     done