import { method } from 'lodash';
import { request } from 'umi';
// import {Former} from './data.d';

const API:string = '/api/trainJobManage';
const ResfreshPath:string='/api/refresh/path'
const AlgoAPI:string='/api/algoManage';
const ResfreshAlgo:string='/api/refresh/algo'
const ResfreshRes:string='/api/refresh/resource'
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
export async function getAlgo(params){
    // params 回传算法列表
    return request(AlgoAPI,{
        method:'GET',
        params,
    });
}
export async function refreshAlgo(params){
    // params 回传算法列表
    let a= request(ResfreshAlgo,{
        method:'GET',
        params,
    });
    // console.log("RETURN is: ",a);
    return a;
}
export async function refreshResource(params){
    return request(ResfreshRes,{
        method:'GET',
        params,
    });
}
// export async function 