import React, { Children ,useState } from 'react';
import { Redirect } from 'umi';
import { 
    Card, 
    Typography, 
    Alert, 
    Button, 
    Divider,
    Form, 
    Radio, 
    Space, 
    Cascader,
    Switch,
  } from 'antd';
import { NumberOutlined } from '@ant-design/icons';

import { PageContainer } from '@ant-design/pro-layout';
import ProForm, {
    StepsForm,
    ProFormText,
    ProFormDatePicker,
    ProFormSelect,
    ProFormTextArea,
    ProFormCheckbox,
    ProFormDateRangePicker,
    ProFormSwitch,
  } from '@ant-design/pro-form';
import ProCard from '@ant-design/pro-card';
import type { ProColumns } from '@ant-design/pro-table';
import { EditableProTable } from '@ant-design/pro-table';

import ProField from '@ant-design/pro-field';
import { ProFormRadio } from '@ant-design/pro-form';

import { message } from 'antd';
import { history } from 'umi';

import {InputConstraint,PathSelector} from './components';
import { postForm } from './service';
import { values } from 'lodash';
// import {postForm, getDataset} from './service';
// 测试用的 Options 数据
const EngingOptions=[
  {
    value:"Pytorch",
    label:"Pytorch",
    children:[
      {
        value:"0.8",
        label:"0.8",
      },
      {
        value:"1.2",
        label:"1.2",
      },
    ],
  },
  {
    value:"Tensorflow",
    label:"Tensorflow",
    children:[
      {
        value:"1.4",
        label:"1.4",
      },
      {
        value:"2.0",
        label:"2.0",
      },
    ],
  },
];

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
  // {
  //   title:'映射路径',
  //   dataIndex:'path',
  //   renderFormItem:()=><PathSelector />,
  //   // render
  // },
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
    title:'描述',
    dataIndex:'description',
    valueType:'text',
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
  const [createType,setType] = React.useState<number>(0);
  const [ifImport,setImport] = React.useState<number>(0);

  const [ioKeys,setIoKeys] = React.useState<React.Key[]>([]);
  const [ioData,setIoData] = React.useState<ioDataType[]>(()=> defaultIO);
  const [newRecord,setNewRecord] = React.useState({
    id:(Math.random()*1000000)/1,});

  const [outputKeys,setOutput]=React.useState<React.Key[]>([]);
  const [hyperKeys,setHyperKeys] = React.useState<React.Key[]>([]);
  const [hyperList,setHyper] = React.useState<hyperType[]>([]);
  const [testNum,setTestNum] = React.useState<number>(0);

  const changeState= (num:number,setState:any)=>{
    let now=(createType+1)%num;
    console.log("Now is :", now);  
    setState(now);
  };
  
  // const {createType,setType}=React.useState(0);
  let createContent;
  if(createType==0)
  { 
    //此处应为从后台获取AI引擎数据的级联选择器，现在是mock的假数据
    createContent=<>
      <ProForm.Item name="AIEngine" label="AI引擎">
        <Cascader options={EngingOptions} size="middle" />
      </ProForm.Item>
      <ProForm.Item name="CodePath" label="代码目录">
        <PathSelector />
      </ProForm.Item>
      <ProForm.Item name="StartFile" label="启动文件">
        <PathSelector />
      </ProForm.Item>
    </>;
  }
  else
  {
    createContent=<h1>镜像方式创建</h1>;
  }
  // let importParam=<>
  //   <Typography.Text>
  //     参数来源路径 : 工程文件夹下/本地配置文件json
  //   </Typography.Text>
  //   </>;
  let importParam=<></>;
  switch(ifImport)
  {
    case 0:{
      importParam=<></>;
      break;};
    case 1:{
      importParam=<>
        <Typography.Text>
        参数来源路径 : 工程文件夹下配置文件.json
        </Typography.Text>
      </>;
      break;};
    case 2:{
      importParam=<>
        <Typography.Text>
        参数来源路径 : 本地配置文件.json
        </Typography.Text>
      </>;      
      break;};
  }
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
        label="算法名称"
        width="md"
        tooltip="最长为24个字"
        placeholder="请输入名称"
        rules={[{required:true}]}
      />
      <ProFormText
        name="version"
        label="版本"
        width="md"
        rules={[{required:true}]}
      />
      <ProFormTextArea 
        name="description"
        label="算法描述"
        width="lg"
      />
      <Divider />
      <ProForm.Item > 
        <Typography.Text strong> 创建方式 : </Typography.Text>
        <Radio.Group defaultValue={0} buttonStyle="solid"
          onChange={(e)=>setType(e.target.value)}
        >
          <Radio.Button value={0} > 自定义脚本 </Radio.Button>
          <Radio.Button value={1} disabled> 自定义镜像 </Radio.Button>
        </Radio.Group>
      </ProForm.Item>
      {createContent}
      <Divider />
      <ProForm.Item label="超参设置"
        name="hyperParams"
        trigger="onValuesChange"
      >
        <EditableProTable<hyperType>
          rowKey="id"
          maxLength={20}   
          toolBarRender={false}
          columns={hyperCloumns}
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
          >
        </EditableProTable>
      </ProForm.Item>
      <ProForm.Item label="输入输出数据配置" 
        name="inputParams"
        trigger="onValuesChange"
        >
        <EditableProTable<ioDataType>
          rowKey="id"
          maxLength={20}
          value={ioData}
          onChange={setIoData}
          toolBarRender={false}
          columns={ioColumns}
          recordCreatorProps={{
            newRecordType:'dataSource',
            position:'bottom',
            record: () => ({ id: Date.now(),}),
          }}
          editable={{
            type:'multiple',
            editableKeys:ioKeys,
            onChange:setIoKeys,
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