import React, { Children ,useState, useRef } from 'react';
import { Redirect } from 'umi';
import { 
    Typography, 
    Button, 
    Divider,
  } from 'antd';
import { PageContainer } from '@ant-design/pro-layout';
import ProForm, {
    ProFormText,
    ProFormSelect,
    ProFormTextArea,
    ProFormDependency,
  } from '@ant-design/pro-form';
import ProCard from '@ant-design/pro-card';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import { EditableProTable } from '@ant-design/pro-table';

import { message } from 'antd';
import { history } from 'umi';

import {InputConstraint,PathSelector} from './components';
import { postForm, getAlgo, refreshAlgo} from './service';
import {AlgoTableItem} from './data.d';
import { values } from 'lodash';
// import {postForm, getDataset} from './service';

// 数据类型
type ioDataType={
  id:React.Key;
  name?:string;
  label?:string;
  description?:string;
  path?:string;
  children?:ioDataType[];
};
type hyperType={
  id:React.Key;
  name?:string;
  description?:string;
  dataType?:string;
  default?:number|string|boolean;
  necessray?:boolean;
  range?:number[];
  adjustable?:boolean;
};

// 定义表格columns
const ioColumns:ProColumns<ioDataType>[]=[
  {
    title:'映射名称',
    dataIndex:'label',
    valueType:'text',
    width:'20%',
  },
  {
    title:'参数名',
    dataIndex:'name',
    valueType:'text',
    width:'20%',
  },
  {
    title:'描述',
    dataIndex:'label',
    valueType:'text',
    width:'50%',
  },
  {
    title:'映射路径',
    dataIndex:'path',
    renderFormItem:()=><PathSelector />,
    // render
  },
  {
    title:'操作',
    valueType:'option',
  },
]
const hyperCloumns:ProColumns<hyperType>[]=[
  {
    title:'超参名',
    dataIndex:'name',
    valueType:'text',
    width:'20%',
  },
  {
    title:'类型',
    dataIndex:'dataType',
    valueType:'select',
    valueEnum:{
      int:{text:"Int"},
      float:{text:"Float"},
      string:{text:"String"},
      bool:{text:"Boolean"},
    }
    // width:'20%',
  },
  {
    title:'初始值',
    dataIndex:'default',
    valueType:'text',
    // width:'20%',
  },
  {
    title:'必需',
    dataIndex:'necessray',
    valueType:'switch',
    // width:'20%',
  },
  {
    title:'操作',
    valueType:'option',
  },
]
const defaultIO:ioDataType[]=[
  {
    id:100001,
    label:"数据集路径",
  },
  {
    id:100002,
    label:"输出路径",
  },
  ]
// 工具函数
const waitTime = (time: number = 100) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
};
const afterSuccess = () =>
  {
    history.goBack();
  }

export default (): React.ReactNode =>{
  // console.log(props.match.params)
  const [inputKeys,setInputKeys] = React.useState<React.Key[]>([]);
  const [inputData,setInputData] = React.useState<ioDataType[]>(()=> defaultIO);
  const [hyperKeys,setHyperKeys] = React.useState<React.Key[]>([]);
  const [hyperList,setHyper] = React.useState<hyperType[]>([]);
  const [algoID,setAlgoID] = React.useState<number>(0);

  const algoActionRef = useRef<ActionType>();
  const hyperRef = useRef<ActionType>();
  const ioRef = useRef<ActionType>();
  
  const my_algo:ProColumns<AlgoTableItem>[] = [
    {
      title:'选择',
      valueType:'option',
      render:(text, row, index, action)=>{
        // let color="default";
        // if(algoID == row.id)
        //   color="primary";
        let color= algoID == row.id?"primary":"default";
        return(
          <Button
            type={color}
            onClick={(e)=>{
              // console.log(row);
              if(row.id && algoID!= row.id)
              {
                setAlgoID(row.id);
                hyperRef.current?.reload();
                ioRef.current?.reload();
              }
              else if(row.id && algoID == row.id)
              {
                setAlgoID(0);
                hyperRef.current?.reload();
                ioRef.current?.reload();
              }
            }}
          >
            选择
          </Button>
        )
      }
    },
    {
      title: '名称',
      dataIndex: 'name',
      copyable: true,
      tip: '标题过长会自动收缩',
      width: '30%',
      sorter: (a, b) => a > b, //使用何种排序
      render: (_) => <a>{_}</a>,
    },
    {
      title: '版本',//列表列名
      dataIndex: 'version',//回传的数据键名
      valueType: 'text',//
    },
    {
      title: '描述',//列表列名
      dataIndex: 'description',//回传的数据键名
      valueType: 'text',//
      search: false,
    },
    {
      title: '最近编辑于',
      key: 'edited_at',
      dataIndex: 'edited_at',
      valueType: 'date',
      sorter: (a, b) => a > b, //使用何种排序
    },
    {
      title: '创建时间',
      key: 'created_at',
      dataIndex: 'created_at',
      valueType: 'date',
      sorter: (a, b) => a > b, //使用何种排序
    },
    {
      title: '操作',
      key:'option',
      valueType: 'option',
      width:'auto',
      render: (text, row, index, action) => [
        <Button key="2"> 查看 </Button> 
      ],
    },
  ];
  // const [newRecord,setNewRecord] = React.useState({
  //   id:(Math.random()*1000000)/1,});  
  return (
  <PageContainer content="" >
  <ProCard>
    <ProForm
      onFinish={async values => {
        let res=postForm(values);
        let rep={};
        //如果 是 async类型的函数 这里必须加 await 否则会异步执行后面的代码，导致 rep 没有赋值
        await res.then( 
          (resp)=>{
            rep["success"]=resp.success;
            rep["reason"]=resp.errorMessage;
            return resp;
          });
        if(!rep["success"] || rep["success"]=="false"){
          message.error("提交失败");
          message.error(rep["reason"]);
        }
        else{
          afterSuccess();
          message.success('提交成功！');            
        }
        // history 回退到上一层
    }}
    >
      <ProFormText
        name="name"
        label="任务名"
        width="md"
        tooltip="最长为24个字"
        rules={[{required:true}]}
      />
      <ProFormTextArea 
        name="description"
        label="任务描述"
        width="lg"
      />
      <Divider />
      <Typography.Text strong> 选择算法 : </Typography.Text>
      <ProTable
        columns={my_algo}
        actionRef={algoActionRef}
        request={(params, sorter, filter) => 
          getAlgo({ ...params, sorter, filter })
        }
        rowKey="id"
        // search={{
        //   labelWidth: 'auto',
        // }}
        search={false}
        pagination={{
          pageSize: 10,
        }}
        dateFormatter="string"
        // headerTitle="高级表格"
        />
      <Divider />
      {/* <ProFormDependency name={["hello"]}>
        {({name}) =>{
          return (
            <EditableProTable>

            </EditableProTable>
          )
        }}
      </ProFormDependency> */}
      <ProForm.Item label="超参设置"
        name="hyperParams"
        trigger="onValuesChange"
      >
        
        <EditableProTable<hyperType>
          rowKey="id"
          maxLength={20}   
          value={hyperList}
          actionRef={hyperRef}
          toolBarRender={false}
          columns={hyperCloumns}
          onChange={setHyper}
          request={(params, sorter, filter) => 
            refreshAlgo({ ...params, sorter, filter, algo_id:algoID, hyper:true })
          }
          recordCreatorProps={{
            newRecordType:'dataSource',
            position:'bottom',
            record: () => ({ id: Date.now(),}),
          }}
          editable={{
            type:'multiple',
            editableKeys:hyperKeys,
            onChange:setHyperKeys,
            actionRender:(row,_,dom)=>{
              return [dom.delete];
            },
          }}
          />
      </ProForm.Item>
      <ProForm.Item label="输入输出数据配置" 
        name="inputParams"
        trigger="onValuesChange"
        >
        <EditableProTable<ioDataType>
          rowKey="id"
          maxLength={20}
          value={inputData}
          actionRef={ioRef}
          onChange={setInputData}
          toolBarRender={false}
          columns={ioColumns}
          request={(params, sorter, filter) => 
            refreshAlgo({ ...params, sorter, filter, algo_id:algoID, ioput:true })
          }  
          recordCreatorProps={{
            newRecordType:'dataSource',
            position:'bottom',
            record: () => ({ id: Date.now(),}),
          }}
          editable={{
            type:'multiple',
            editableKeys:inputKeys,
            onChange:setInputKeys,
            actionRender:(row,_,dom)=>{
              return [dom.delete];
            },
          }}
        />
      </ProForm.Item>
    </ProForm>
  </ProCard>
  </PageContainer>
  )
};