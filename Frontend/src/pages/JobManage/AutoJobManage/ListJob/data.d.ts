export interface TableItem {
  id:number;
  title:string;
  type:string;
  train_status:string;
  deploy_status:string;
  data_source:string;
  created_at:Date;
  description?:string;
}
export interface TableListParams {
  status?: string;
  name?: string;
  desc?: string;
  key?: number;
  pageSize?: number;
  currentPage?: number;
  filter?: { [key: string]: any[] };
  sorter?: { [key: string]: any };
}