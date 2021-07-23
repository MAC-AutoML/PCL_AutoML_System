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
    ProFormRadio,
  } from '@ant-design/pro-form';
import ProCard from '@ant-design/pro-card';
import ProTable, { ProColumns, ActionType, EditableProTable } 
  from '@ant-design/pro-table';

import { message } from 'antd';
import { history } from 'umi';

import {InputConstraint,PathSelector} from './components';
import { postForm, getAlgo, refreshAlgo, refreshResource} from './service';
import {AlgoTableItem, ioDataType, hyperType} from './data.d';
import { values } from 'lodash';
// import {postForm, getDataset} from './service';

// 数据类型


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
  // {
  //   title:'描述',
  //   dataIndex:'label',
  //   valueType:'text',
  //   width:'10%',
  // },
  {
    title:'映射路径',
    dataIndex:'path',
    width:'50%',
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
    title:'值',
    dataIndex:'default',
    valueType:'text',
    // editable:true,
    // width:'20%',
  },
  // {
  //   title:'必需',
  //   dataIndex:'necessray',
  //   valueType:'switch',
  //   // width:'20%',
  // },
  {
    title:'操作',
    valueType:'option',
  },
]
// 工具函数
const afterSuccess = () => history.goBack();

export default (): React.ReactNode =>{
  // console.log(props.match.params)
  const [ioKeys,setIoKeys] = React.useState<React.Key[]>([]);
  const [ioData,setIoData] = React.useState<ioDataType[]>([]);
  const [hyperKeys,setHyperKeys] = React.useState<React.Key[]>([]);
  const [hyperList,setHyper] = React.useState<hyperType[]>([]);
  const [algoID,setAlgoID] = React.useState<number>(0);
  // const [table,setTable] React.useState<React.ReactNode>(<></>);


  const algoActionRef = useRef<ActionType>();
  const hyperRef = useRef<ActionType>();
  const ioRef = useRef<ActionType>();

  const HyperTable= (ID:number)=>
    <EditableProTable<hyperType>
    key={ID}
    rowKey="id"
    maxLength={20}   
    value={hyperList}
    actionRef={hyperRef}
    columns={hyperCloumns}
    onChange={setHyper}
    toolBarRender={false}
    controlled={true}
    request={(params, sorter, filter) => {
      let pro=refreshAlgo({ ...params, sorter, filter, algo_id:ID, hyper:true });
      let data=[];
      let ids:number[]=[];
      pro.then(
        (resp)=>{
          data=resp.data;
          for(let k in data)
            ids.push(data[k].id);
          setHyperKeys([...hyperKeys,...ids])
          return resp;
        });
      return pro;
    }}
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
  var HPYER_TABLE=HyperTable(algoID);
  const IOTable=(ID:number)=>
    <EditableProTable<ioDataType>
      key={ID}
      rowKey="id"
      maxLength={20}
      value={ioData}
      actionRef={ioRef}
      columns={ioColumns}
      onChange={setIoData}
      toolBarRender={false}
      controlled={true}
      request={(params, sorter, filter) => {
        let pro=refreshAlgo({ ...params, sorter, filter, algo_id:ID, ioput:true });
        let data=[];
        let ids:number[]=[];
        pro.then(
          (resp)=>{
            data=resp.data;
            for(let k in data)
              ids.push(data[k].id);
            setIoKeys([...ioKeys,...ids])
            return resp;
          });
        return pro;
      }
      }  
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
  var IO_TABLE=IOTable(algoID);
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
              setHyper([]);
              setHyperKeys([]);
              setIoKeys([]);
              setIoData([]);
              if(row.id && algoID!= row.id)
                setAlgoID(row.id);
              else if(row.id && algoID == row.id)
                setAlgoID(0);
              console.log("ALGO is: ",row);
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

  return (
  <PageContainer content="" >
  <ProCard>
    <ProForm
      onFinish={async (values) => {
        // console.log("FORMS: ",values);
        // console.log("HYPER: ",hyperList);
        // console.log("IOPAR: ",ioData);
        // 这里定义了一部分的回传键值对
        let res=postForm({
            ...values,
            algoID:algoID,
            hyperDict:hyperList,
            ioDict:ioData});
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
          getAlgo({ ...params, sorter, filter })}
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
      <ProForm.Item 
        // name="hyperTable"
        // trigger="onValuesChange"
        >
      <Typography.Text strong> 超参数设置 : </Typography.Text>
        {HPYER_TABLE}
      </ProForm.Item>
      <ProForm.Item 
        // name="ioTable"
        trigger="onValuesChange"
      >
      <Typography.Text strong> 输入输出路径 : </Typography.Text>
        {IO_TABLE}
      </ProForm.Item>
      <Divider />
      {/* 资源选择 */}
      <Typography.Text strong> 资源选择 : </Typography.Text>
      {/* 遍历返回值， 制造一组 radio groups */}
      <ProForm.Item>
        <ProFormSelect
          name = "resource"
          request={(_)=>refreshResource(_)}
          rules={[{ required: true, message: 'Please select Resource!' }]}
        />
      </ProForm.Item>

    </ProForm>
  </ProCard>
  </PageContainer>
  )
};