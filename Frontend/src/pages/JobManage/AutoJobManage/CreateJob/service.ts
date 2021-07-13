import { method } from 'lodash';
import { request } from 'umi';
// import {Former} from './data.d';

const API:string = '/api/autoJobManage';
const ResfreshAPI:string='/api/refresh/';
const ResfreshPath:string='/api/refresh/path'
export async function postForm(params){
    return request(API,{
        method: 'POST',
        data: params,
    });
}
export async function getForm(params){
    return request( API,{
        method:'GET', 
        data: params,
    });
}
export async function getPath(params:string){
    // params 回传任务类型
    let result=await request(ResfreshPath,{
        method: 'GET',
        params:params,
    })
    return result;
}
// export async function 