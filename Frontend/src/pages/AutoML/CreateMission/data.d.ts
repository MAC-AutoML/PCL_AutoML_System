export interface Former {
    //Base set
    type:string;
    name:string;
    description?:string;
    //Dataset set
    dataName?:string;
    dataOutput?:string;
    dataInput?:string;
    // 已有数据集的id
    dataSelection?:string;
    //Model set
    modelsize:number;
}

export interface SelectItem {
    label:string;
    value:string;
}
