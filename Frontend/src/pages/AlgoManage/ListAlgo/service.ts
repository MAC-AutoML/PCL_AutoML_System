import { request } from 'umi';
import {TableItem,TableListParams} from './data.d';

const API:string = '/api/algoManage';

export async function queryMission(params:TableListParams){
    return request(API,{
        method: 'GET',
        params,
    });
}
export async function deleteMission(params:TableItem){
    // let info={DELETE: '', ...params};
    // console.log("INFO is: ",info);
    return request(API,{
        method: 'DELETE',
        data:params, // DELETE POST 要用 data: param, GET 要用 params:
    });
}
// export async function 