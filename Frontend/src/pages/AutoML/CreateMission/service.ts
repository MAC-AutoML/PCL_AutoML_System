import { method } from 'lodash';
import { request } from 'umi';
import {Former} from './data.d';

const API:string = '/api/automl';
const ResfreshAPI:string='/api/refresh/';
const ResfreshDataset:string=ResfreshAPI+'dataset'
export async function postForm(params:Former){
    return request(API,{
        method: 'POST',
        data: params,
    });
}
export async function getDataset(params:string){
    // params 回传任务类型
    return request(ResfreshDataset,{
        method: 'GET',
        params:{'type':params},
    })
}
// export async function 