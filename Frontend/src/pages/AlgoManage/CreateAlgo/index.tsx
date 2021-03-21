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
  path?;
  children?:ioDataType[];
};
type hpyerType={
  name:string;
  description?:string;
  dataType:string;
  range?:number[];
  adjustable:boolean;
  default:number;
  necessray:boolean;
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

  const [inputKeys,setInputKeys] = React.useState<React.Key[]>([]);
  const [inputData,setInputData] = React.useState<ioDataType[]>([]);
  const [newRecord,setNewRecord] = React.useState({
    id:(Math.random()*1000000)/1,});

  const [outputKeys,setOutput]=React.useState<React.Key[]>([]);
  const [hyperList,setHyper] = React.useState<string[]>([]);
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
    //此处应为从后台获取AI引擎数据的级联选择器
    createContent=<>
      <Form.Item name="AIEngine" label="AI引擎">
        <Cascader options={EngingOptions} />
      </Form.Item>
      <Form.Item name="CodePath" label="代码目录">
        <PathSelector />
      </Form.Item>
      <Form.Item name="StartFile" label="启动文件">
        <PathSelector />
      </Form.Item>
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
  <StepsForm
			onFinish={async (values)=>{

				await waitTime(200);
				message.success("提交成功");
        let res = postForm(values);
				console.log(values);
        afterSuccess();
			}}
		formProps={{
			validateMessages:{
				required:'此项为必填项',
			},
		}}
		>
			<StepsForm.StepForm
        name="train"
        title="训练规范"
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
        <Form.Item > 
          <Typography.Text strong> 创建方式 : </Typography.Text>
          <Radio.Group defaultValue={0} buttonStyle="solid"
            onChange={(e)=>setType(e.target.value)}
          >
            <Radio.Button value={0} > 自定义脚本 </Radio.Button>
            <Radio.Button value={1} disabled> 自定义镜像 </Radio.Button>
          </Radio.Group>
        </Form.Item>
        {createContent}
        <Divider />
        <ProForm.Item label="输入数据配置" 
          name="inputParams"
          trigger="onValuesChange"
          >
          {/* {console.log("Editable ProTable")} */}
          <EditableProTable<ioDataType>
            rowKey="id"
            maxLength={20}
            toolBarRender={false}
            columns={ioColumns}
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
        <Divider />
          {/* <DynamicForm /> */}
        <ProForm.Item label="输出数据配置" 
          name="outputParams"
          trigger="onValuesChange"
          >
          <EditableProTable<ioDataType>
          rowKey="id"
          maxLength={20}
          toolBarRender={false}
          columns={ioColumns}
          recordCreatorProps={{
            newRecordType:'dataSource',
            position:'bottom',
            // record: {id: Date.now(),},
            record: () => ({ id: Date.now(),}),
          }}
          editable={{
            type:'multiple',
            editableKeys:outputKeys,
            onChange:setOutput,
            actionRender:(row,_,dom)=>{
              return [dom.delete];
            },
          }}
          />
        </ProForm.Item>
        <Divider />
      </StepsForm.StepForm>
			<StepsForm.StepForm
        name="hpyer"
        title="超参规范"
      >
        <Typography>
          <Typography.Title level={4}>定义超级参数</Typography.Title>
          <Typography.Paragraph>
            使用该算法创建训练作业时，以下超级参数支持用户查阅或修改，
            最终会在启动命令中，以命令行参数的形式传入您的训练脚本或镜像中
          </Typography.Paragraph>
        </Typography>
        <Button.Group size="middle">
        <Button>删除</Button>
        <Button>修改</Button>
        <Button>清空</Button>
        </Button.Group>
        <Divider />
        <Form.Item>
          <Typography.Text strong> 从文件导入参数 : </Typography.Text>
          {/* <Switch 
            onChange= {(checked:boolean,event)=>{
              console.log("checked",checked);
              setImport(checked)
            }}
            defaultChecked={false}
          /> */}
          <Radio.Group defaultValue={0} buttonStyle="solid"
            onChange={(e)=>setImport(e.target.value)}
          >
            <Radio.Button value={0} > 页面输入 </Radio.Button>
            <Radio.Button value={1} > 远程文件导入 </Radio.Button>
            <Radio.Button value={2} > 本地文件导入 </Radio.Button>
          </Radio.Group>
        </Form.Item>
        {importParam}
        <Divider />
        {/* <DynamicForm /> */}
      </StepsForm.StepForm>
			<StepsForm.StepForm
        name="constrain"
        title="使用约束"
      >
        <InputConstraint />
      </StepsForm.StepForm>
			<StepsForm.StepForm
        name="finish"
        title="完成"
      >

      </StepsForm.StepForm>
		</StepsForm>
  </ProCard>
  </PageContainer>
  )
};