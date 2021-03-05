export interface AlgorithmItem {
    id:number;
    name:string;
    task:string;
    createUser?:string;
    createUserId?:number;
    createTime?:Date;
    path?:string;// 【】扩展为readme.md等的路径
}