import { method } from 'lodash';
import { request } from 'umi';
// import {Former} from './data.d';

const API:string = '/api/algoManage';
const ResfreshAPI:string='/api/refresh/';
const ResfreshPath:string=ResfreshAPI+'path'
export async function postForm(params){
    return request(API,{
        method: 'POST',
        data: params,
    });
}
export async function getPath(params:Array<string>){
    // params 回传任务类型
    let result=await request(ResfreshPath,{
        method: 'GET',
        params:params,
    })
    return result;
}
// export async function 