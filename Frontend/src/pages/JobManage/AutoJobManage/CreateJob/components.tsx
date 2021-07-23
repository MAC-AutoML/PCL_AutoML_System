import React, { Props, useState } from 'react';
import {useRequest} from 'umi';
import { Card, Typography, Alert, Button,Cascader, Row,Col, Divider,
		Form, Table, Input, InputNumber, Popconfirm, AutoComplete
	} from 'antd';
import ProForm, {ProFormSelect} from '@ant-design/pro-form';
import { ColumnsState, EditableProTable } from '@ant-design/pro-table';
import type { ProColumns } from '@ant-design/pro-table';

import {refreshPath} from './service';
import Item from 'antd/lib/list/Item';
const {Option} = AutoComplete;
// interface ProviderProps {
// 	value?:{ key:string;label:string;}[];
// 	onChange?:(
// 		value:{key:string;label:string;}[],
// 	)=>void;
// };
interface ProviderProps {
	value?:string;
	onChange?:(
		value:string,
	)=>void;
};
interface PathType {
	value:string,
	label:string,
	isLeaf:boolean,
	children?:PathType,
}
const test=[{
	value:"init0",
	label:"init0",
	isLeaf:false,
},{
	value:"init1",
	label:"init1",
	isLeaf:false,
}];
// interface 定义部件参数名和类型 React.FC<ParamList>
//仿照 VScode 选择路径的方式来, 基于antd select 模组
/* ----------------------------------------------------------- */
const PathSelector:React.FC<ProviderProps>=({value,onChange})=>{
	let p:string[]=[];
	const [pathList, setPathList] = useState(p);
	const [inputPath,setInputPath]=useState<string>("");
	const handleChange = (changedValue:string)=>{
		// 从后台请求数据 ， 需要加防抖功能
		let promise=refreshPath(changedValue);
		promise.then(
			(resp)=>{
				setPathList(resp.data);
				return resp;}
		);
		// console.log("CHANGEDVALUE is : ",changedValue);
		setInputPath(changedValue);
		onChange?.(changedValue);
	};
	const handleFocus = ()=>{
		if(inputPath=="")
			handleChange("");
	}
	const handleSelect = (changedValue:string)=>{
		let i = changedValue.lastIndexOf("..");
		if(i>-1)
			changedValue=changedValue.slice(0,i);
		let j = changedValue.lastIndexOf("/");
		if(i==j+1)
		{
			var k=changedValue.slice(0,j).lastIndexOf("/");
			var temp=changedValue.slice(0,k+1);
			changedValue=temp;
		}
		handleChange(changedValue);
	}
	return <AutoComplete 
		style={{width:350}} 
		value={inputPath}
		onChange={handleChange} 
		onFocus={handleFocus}
		onSelect={handleSelect}
		> 
		{
			pathList.map(
				(pathStr)=>{
					// return <Option key={pathStr} value={pathStr} > {pathStr} </Option>;
					// 这里假设返回的是文件的绝对路径(相对于分配给用户的根目录)
					let v:number=pathStr.lastIndexOf("/");
					let label=pathStr;
					if (v+1<pathStr.length)
						label=pathStr.slice(v+1);
					else if (v+1==pathStr.length)
					{
						var k=pathStr.slice(0,v).lastIndexOf("/");
						label=k>0? pathStr.slice(k+1): label;
					}						
					return <Option key={pathStr} value={pathStr} > {label} </Option>;
				}
			)
		}
	</AutoComplete>
}
/* ----------------------------------------------------------- */
interface InputProps{

};
// valueEnum 类型的预定义数据,待修改为从后台获取数据
const sourceOptions=[
	{label: "数据存储位置", value : 'selfDataset'},
	{label: "PCL数据集", value : 'officialDataset'},
];
const labelOptions=[
	//使用全局设置json中的任务类型value
	{label: "物体检测", value : 'ObjectDetection'},
	{label: "图像分类", value : 'ImageClassification'},
];
const formOptions=[
	{label: "默认格式", value : 'default'},
	{label: "CarbonData", value : 'carbonData'},
];
const splitOptions=[
	{label: "仅支持切分数据集", value : 'split'},
	{label: "仅支持未切分数据集", value : 'unsplit'},
	{label: "无限制", value : 'unlimit'},
];
const inputList=[
	"inputer1","inputer2","inputer3",
]
const InputConstraint:React.FC<InputProps>=(props)=>{
	const [selector,setSelect] = React.useState<string[]>([]);
	const getSource= async ()=> sourceOptions;
	const getLabel= async ()=>labelOptions;
	const getForm= async ()=>formOptions;
	const getSplit= async ()=>splitOptions;
	let inputlist=inputList;
	let others=<></>;
	let Pname="输入路径1";
	if(selector.includes(sourceOptions[1].value))
	{
		others=<>
			<Divider /> 
			<Typography.Title level={4}>{Pname}</Typography.Title>
			<Row><Col>{/* 没起到分栏分行作用，需要进一步研究 */}
				<Typography.Text>按"训练规范-输入数据配置"部件传入的参数列表循环列出</Typography.Text>	
			</Col></Row>
			<Row><Col>
				<ProFormSelect
					name={ Pname.toString()+"_"+"labelType"} width="xl"
					label="标注类型"
					allowClear
					request={getLabel}
				/>
			</Col></Row>
			<Row><Col>
				<ProFormSelect
					name="formType" width="xl"
					label="数据格式"
					allowClear
					request={getForm}
				/>
			</Col></Row>
			<Row><Col>
				<ProFormSelect
					name="splitType" width="xl"
					label="数据切分"
					allowClear
					request={getSplit}
				/>
			</Col></Row>
			<Divider />
		</>;
		
	}
	else
	{
		others=<></>;
	}
	return <>
		<ProFormSelect 
			name="dataSource" width="xl"
			label="数据来源"
			mode="multiple"
			allowClear
			request={getSource}
			fieldProps={{
				onChange:(value)=>setSelect(value),
			}}
		/>
		{others}
	</>;
};
export {InputConstraint,PathSelector};

// for (let index = 0; index < inputlist.length; index++) {
// 	let element = inputlist[index];
// 	<Typography.Title level={4}>{Pname}</Typography.Title>
// 	<Row><Col>{/* 没起到分栏分行作用，需要进一步研究 */}
// 		<Typography.Text>按部件传入的参数列表循环列出</Typography.Text>	
// 	</Col></Row>
// 	<Row><Col>
// 		<ProFormSelect
// 			name={ Pname.toString()+"_"+"labelType"} width="xl"
// 			label="标注类型"
// 			allowClear
// 			request={getLabel}
// 		/>
// 	</Col></Row>
// 	<Row><Col>
// 		<ProFormSelect
// 			name="formType" width="xl"
// 			label="数据格式"
// 			allowClear
// 			request={getForm}
// 		/>
// 	</Col></Row>
// 	<Row><Col>
// 		<ProFormSelect
// 			name="splitType" width="xl"
// 			label="数据切分"
// 			allowClear
// 			request={getSplit}
// 		/>
// 	</Col></Row>
// 	<Divider />			
// 	}