import { request } from 'umi';
import {  } from './data.d';

const API:string='/api/AImarket';

export async function queryAlgorithms(par){
    // return request(API,{
    //     method:'GET',
    //     params:par,
    // });
    return request(API,{
        method:'POST',
        data:par,
    });
}