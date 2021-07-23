export interface Former {
	// Base Info
    
}
export interface AlgoTableItem{
	id?:number;
	name?: string;
	version?: string;
	description?: string;
	created_at?: string;
	edited_at?: Date;
};
export interface ioDataType{
	id:React.Key;
	name?:string;
	label?:string;
	description?:string;
	path?:string;
	children?:ioDataType[];
};
export interface hyperType {
	id:React.Key;
	name?:string;
	description?:string;
	dataType?:string;
	default?:number|string|boolean;
	necessray?:boolean;
	// range?:number[];
	adjustable?:boolean;
	// search used 
	space?:string;
	searchType?:string;
	content?:string;
};
export interface searchType {
	id:React.Key;
	name?:string;
	dataType:string;
	default?:number|string|boolean;
	searchType?:string;
	content?:string;

}