import React, { Children ,useState, useRef } from 'react';
import { Redirect } from 'umi';
import { 
    Typography, 
    Button, 
    Divider,
    Select,
  } from 'antd';
import { PageContainer } from '@ant-design/pro-layout';
import ProForm, {
    ProFormText,
    ProFormSelect,
    ProFormTextArea,
    ProFormRadio,
    ProFormDigit,
  } from '@ant-design/pro-form';
import ProCard from '@ant-design/pro-card';
import ProTable, { ProColumns, ActionType, EditableProTable } 
  from '@ant-design/pro-table';

import { message } from 'antd';
import { history } from 'umi';

import {InputConstraint,PathSelector} from './components';
import { postForm, getAlgo, refreshAlgo, refreshResource, refreshMethod} from './service';
import {AlgoTableItem, ioDataType, hyperType, searchType} from './data.d';
import { once, values } from 'lodash';
import { stringify } from 'qs';
import { getOverflowOptions } from 'antd/lib/tooltip/placements';
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

// 工具函数
const afterSuccess = () => history.goBack();

export default (): React.ReactNode =>{
  // console.log(props.match.params)
  const [ioKeys,setIoKeys] = React.useState<React.Key[]>([]);
  const [ioData,setIoData] = React.useState<ioDataType[]>([]);
  const [hyperKeys,setHyperKeys] = React.useState<React.Key[]>([]);
  const [hyperData,setHyperData] = React.useState<hyperType[]>([]);
  const [algoID,setAlgoID] = React.useState<number>(0);
  // const [table,setTable] React.useState<React.ReactNode>(<></>);
  const [searchKeys,setSearchKeys] = React.useState<React.Key[]>([]);
  const [searchData,setSearchData] = React.useState<hyperType[]>([]);

  const algoActionRef = useRef<ActionType>();
  const hyperRef = useRef<ActionType>();
  const ioRef = useRef<ActionType>();
  const searchRef = useRef<ActionType>();

  const hyperColumns:ProColumns<hyperType>[]=[
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
    {
      title:'操作',
      valueType:'option',
    },
  ]
  
  const HyperTable= (ID:number)=>
    <EditableProTable<hyperType>
    key={ID}
    rowKey="id"
    maxLength={20}   
    value={hyperData}
    actionRef={hyperRef}
    columns={hyperColumns}
    onChange={setHyperData}
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
      actionRender:(row, config, dom)=>{
        return [
          <Button id={String(row.id)+"del"} key={0} danger>
            {dom.delete}
          </Button>, 
          <Button id={String(row.id)+"cha"} key={1}
          onClick={(e)=>{
            setSearchKeys([...searchKeys,row.id]);
            setSearchData([...searchData,row]);
            let i=0;
            for( i=0 ; i<hyperKeys.length;i++)
              if(hyperKeys[i]==row.id) break;
            setHyperKeys([
              ...hyperKeys.slice(0,i),...hyperKeys.slice(i+1)
            ]);
            // hyperList.splice(i,1);
            setHyperData([
              ...hyperData.slice(0,i),...hyperData.slice(i+1)
            ]);
          }}
        >加入搜索</Button>
      ];},
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
  const searchColumns:ProColumns<hyperType>[]=[
    {
      title:'参数名',
      dataIndex:'name',
      valueType:'text',
      width:'20%',
      editable:false,
    },
    {
      title:'参数类型',
      dataIndex:'dataType',
      valueType:'select',
      valueEnum:{
        int:{text:"Int"},
        float:{text:"Float"},
        string:{text:"String"},
        bool:{text:"Boolean"},
      },
      editable:false,
      // width:'20%',
    },
    {
      title:'取值方式',
      dataIndex:'searchType',
      valueType:'radioButton',
      valueEnum:{
        values:{text:"枚举"},
        range:{text:"范围"},
      },
    },
    {
      title:'取值范围',
      dataIndex:'content',
      renderFormItem:(a,b,c)=>{
      var res=<></>;
      if(a.entry.searchType == 'range')
        res=<Select
          key={String(a.entry.id)+"select"}
          name="space"
          label="space"
          options={[
            {'label':'linear','value':'linear'},
            {'label':'log'   ,'value':'log'   },
            {'label':'logit' ,'value':'logit' },
            {'label':'bilog' ,'value':'bilog' },            
          ]}
          // valueEnum={{
          //   linear: 'linear',
          //   log   : 'log',
          //   logit : 'logit',
          //   bilog : 'bilog',
          // }}
          rules={[{ required: true, message: 'Please select your country!' }]}
          onSelect={(value,option)=>{
            for(let i in searchData)
              if(searchData[i].id==a.entry.id)
              {
                var temp=JSON.parse(JSON.stringify(searchData[i]));
                temp.space=value;
                setSearchData([
                  ...searchData.slice(0,i),
                  temp,
                  ...searchData.slice(i+1),
                ])
                break;
              }
          }}
        />
      return <ProForm.Item>
      {res}
      <ProFormTextArea
        key={String(a.entry.id)+"text"}
        label={"以空格分隔数字"}
        tooltip={"枚举模式下，取所有数字。\n范围模式下,取前两数作为上下界"}
      /></ProForm.Item>},
      // renderFormItem:(a,b,c)=><><Button 
      //   onClick={(e)=>{
      //     console.log("a: ",a);
      //     console.log("b: ",b);
      //     console.log("c: ",c);
      //   }}
      // >啥</Button></>,
      width:'30%',
    },
    {
      title:'操作',
      valueType:'option',
    },    
  ]
  const SearchTable=(ID:number)=>
    <EditableProTable<hyperType>
    key={ID}
    rowKey="id"
    maxLength={20}   
    value={searchData}
    actionRef={searchRef}
    columns={searchColumns}
    onChange={setSearchData}
    toolBarRender={false}
    controlled={true}
    recordCreatorProps={false}
    editable={{
      type:'multiple',
      editableKeys:searchKeys,
      onChange:setSearchKeys,
      actionRender:(row, config, dom)=>{
        return [
          <Button id={String(row.id)+"del"} key={0} danger>
            {dom.delete}
          </Button>, 
          <Button id={String(row.id)+"cha"} key={1}
          onClick={(e)=>{
            setHyperKeys([...hyperKeys,row.id]);
            setHyperData([...hyperData,row]);
            let i=0;
            for( i=0 ; i<searchKeys.length;i++)
              if(searchKeys[i]==row.id) break;
            setSearchKeys([
              ...searchKeys.slice(0,i),...searchKeys.slice(i+1)
            ]);
            // searchList.splice(i,1);
            setSearchData([
              ...searchData.slice(0,i),...searchData.slice(i+1)
            ]);
          }}
        >取消搜索</Button>
      ];},
    }}
    />
  var SEARCH_TABLE=SearchTable(algoID);
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
              setHyperData([]);
              setHyperKeys([]);
              setIoKeys([]);
              setIoData([]);
              setSearchKeys([]);
              setSearchData([]);
              if(row.id && algoID!= row.id)
                setAlgoID(row.id);
              else if(row.id && algoID == row.id)
                setAlgoID(0);
              // console.log("ALGO is: ",row);
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
            'algo':{
              'id':algoID,
              'hyperDict':hyperData,
              'ioDict':ioData,
            },
            'search_para':searchData,            
            });
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
      <Divider />
      <ProForm.Item 
        // name="ioTable"
        trigger="onValuesChange"
      >
      <Typography.Text strong> 搜索参数设置 </Typography.Text>
      <ProFormSelect label="搜索方法" name="method"
        request={(_)=>refreshMethod(_)}  required
      />
      <ProFormDigit label="搜索轮数" name="epoch" required />
      <ProFormDigit label="采样数" name="suggest" required />
      <ProFormText label= "Result.txt 路径" name="result" required  />
      <Typography.Text > 搜索参数范围 : </Typography.Text>
      {SEARCH_TABLE}
      </ProForm.Item>
      <Divider />
      <ProForm.Item 
        // name="ioTable"
        trigger="onValuesChange"
      >
      <Typography.Text strong> 输入输出路径 : </Typography.Text>
        {IO_TABLE}
      </ProForm.Item>
      <Divider />
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