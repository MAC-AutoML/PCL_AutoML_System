import { request } from 'umi';
import {TableItem,TableListParams} from './data.d';

const API:string = '/api/automl';

export async function queryMission(params:TableListParams){
    return request(API,{
        method: 'GET',
        params,
    });
}
// export async function 