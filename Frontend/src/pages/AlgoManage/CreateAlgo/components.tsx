import React, { Props, useState } from 'react';
import { Card, Typography, Alert, Button,Cascader, Row,Col, Divider,
		Form, Table, Input, InputNumber, Popconfirm,
	} from 'antd';
import ProForm, {ProFormSelect} from '@ant-design/pro-form';
import { ColumnsState, EditableProTable } from '@ant-design/pro-table';
import type { ProColumns } from '@ant-design/pro-table';

import {getPath} from './service';
import Item from 'antd/lib/list/Item';

interface ProviderProps {
	label:string,
	disable:boolean,
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
//需要换一种方式, Cascader 方式不好
//仿照 VScode 选择路径的方式来, 基于antd select 模组
const PathProvider:React.FC<ProviderProps>=(props)=>{
	// 解包参数
	const {label,disable}=props;
	const [pathes,setPathes]=React.useState(test);
	const onChange=(value,selectedPath) =>{
		console.log("Value: ",value);
		console.log("Selected: ",selectedPath);
	};
	const loadData= selectedPath => {
		const targetOption = selectedPath.length ? selectedPath[selectedPath.length-1] : selectedPath ;
		targetOption.loading=true;
		// console.log("loading selected: ",selectedPath);
		// console.log("loading target: ",targetOption);
		let sender= selectedPath.map((item:PathType)=>{return item.value;});
		// let root=sender.join("/");
		// console.log("loading root: ", root);
		// console.log("loading sender:",sender);
		let nextLevel=getPath(sender);
		// console.log(selectedPath,nextLevel);
		targetOption.children=[
			{
				label:"a",
				value:"a",
				isLeaf:false,
			},
			{
				label:"b",
				value:"b",
				isLeaf:false,
			},
		];
		targetOption.loading=false;
		// nextLevel.forEach(element => {
		// 	targetOption.children
		// });
		// targetOption.children = nextLevel;
		setPathes([...pathes]);
	};
	
	return(
		<Cascader options={pathes} loadData={loadData} 
			onChange={onChange} changeOnSelect disabled={disable}/>
	);
};
/* ----------------------------------------------------------- */
interface Item {
	key: string;
	name: string;
	age: number;
	address: string;
  }
interface EditableCellProps extends React.HTMLAttributes<HTMLElement> {
	editing: boolean;
	dataIndex: string;
	title: any;
	inputType: 'number' | 'text';
	record: Item;
	index: number;
	children: React.ReactNode;
}
const EditableCell: React.FC<EditableCellProps> = ({
  editing,
  dataIndex,
  title,
  inputType,
  record,
  index,
  children,
  ...restProps
}) => {
  const inputNode = inputType === 'number' ? <InputNumber /> : <Input />;

  return (
    <td {...restProps}>
      {editing ? (
        <Form.Item
          name={dataIndex}
          style={{ margin: 0 }}
          rules={[
            {
              required: true,
              message: `Please Input ${title}!`,
            },
          ]}
        >
          {inputNode}
        </Form.Item>
      ) : (
        children
      )}
    </td>
  );
};

const EditableTable = (props) => {
  const [form] = Form.useForm();
  const [data, setData] = useState<Item[]>([]);
  const [editingKey, setEditingKey] = useState('');

  const isEditing = (record: Item) => record.key === editingKey;

  const edit = (record: Partial<Item> & { key: React.Key }) => {
    form.setFieldsValue({ name: '', age: '', address: '', ...record });
    setEditingKey(record.key);
  };
	const add=() =>{
		
	};
  const cancel = () => {
    setEditingKey('');
  };

  const save = async (key: React.Key) => {
    try {
      const row = (await form.validateFields()) as Item;

      const newData = [...data];
      const index = newData.findIndex(item => key === item.key);
      if (index > -1) {
        const item = newData[index];
        newData.splice(index, 1, {
          ...item,
          ...row,
        });
        setData(newData);
        setEditingKey('');
      } else {
        newData.push(row);
        setData(newData);
        setEditingKey('');
      }
    } catch (errInfo) {
      console.log('Validate Failed:', errInfo);
    }
  };

  const columns = [
    {
      title: 'name',
      dataIndex: 'name',
      width: '25%',
      editable: true,
    },
    {
      title: 'age',
      dataIndex: 'age',
      width: '15%',
      editable: true,
    },
    {
      title: 'address',
      dataIndex: 'address',
      width: '40%',
      editable: true,
    },
    {
      title: 'operation',
      dataIndex: 'operation',
      render: (_: any, record: Item) => {
        const editable = isEditing(record);
        return editable ? (
          <span>
            <a href="javascript:;" onClick={() => save(record.key)} style={{ marginRight: 8 }}>
              Save
            </a>
            <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
              <a>Cancel</a>
            </Popconfirm>
          </span>
        ) : (
          <Typography.Link disabled={editingKey !== ''} onClick={() => edit(record)}>
            Edit
          </Typography.Link>
        );
      },
    },
  ];

  const mergedColumns = columns.map(col => {
    if (!col.editable) {
      return col;
    }
    return {
      ...col,
      onCell: (record: Item) => ({
        record,
        inputType: col.dataIndex === 'age' ? 'number' : 'text',
        dataIndex: col.dataIndex,
        title: col.title,
        editing: isEditing(record),
      }),
    };
  });

  return (
    <Form form={form} component={Form.Item}>
      <Table
        components={{
          body: {
            cell: EditableCell,
          },
        }}
        bordered
        dataSource={data}
        columns={mergedColumns}
        rowClassName="editable-row"
        pagination={{
          onChange: cancel,
        }}
      />
    </Form>
  );
};
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
				<Typography.Text>按部件传入的参数列表循环列出</Typography.Text>	
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
export {PathProvider,EditableTable,InputConstraint,};

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