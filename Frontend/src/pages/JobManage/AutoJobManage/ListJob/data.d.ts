export interface TableItem{
  id?:number;
  name?: string;
  version?: string;
  description?: string;
  created_at?: string;
  edited_at?: Date;
}
export interface TableListParams {
    name?: string;
    version?: string;
    desc?: string;
    key?: number;
    pageSize?: number;
    currentPage?: number;
    filter?: { [key: string]: any[] };
    sorter?: { [key: string]: any };
  }