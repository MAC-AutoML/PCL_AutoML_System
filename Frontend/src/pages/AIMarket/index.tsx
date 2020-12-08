import React, { useState } from 'react';
import {
  Card, 
  List,
  Input,
  Select,
  Row, Col
 } from 'antd';

import ProCard from '@ant-design/pro-card';
import { QueryFilter, 
  ProFormText, 
  ProFormDatePicker,
  ProFormDateRangePicker,
  ProFormSelect,
  LightFilter
 } 
  from '@ant-design/pro-form';

import { AlgorithmItem } from './data.d';
import {queryAlgorithms} from './service';
import ExportComponent from '@ant-design/pro-form/lib/components/DatePicker';
import { values } from 'lodash';

// // 【】需要 - 第一次加载时从后端获取一次数据

const {Option} = Select;

// 【】待改成 从后端获取任务类型
const mission_type=[
  {label:"图像分类", value:"Image_Classification",},
  {label:"目标检测", value:"Object_Dectection",},
  {label:"预测分析", value:"Predict_Analysis",},
  {label:"音频分类", value:"Voice_Classfication",},
  {label:"文本分类", value:"Text_Classification",},
]
function handleChange(value) {
  console.log(`selected ${value}`);
};

export default ():React.ReactNode =>{ 

  let initial:AlgorithmItem[]=[];
   queryAlgorithms({"key":"hhhhh"}).then(
    (values)=>{
      let temp:AlgorithmItem[]=[];
      for(let i in values.data)
        temp.push(values.data[i]);
      initial=temp;
      console.log(values.data);
      return values;
    }
  );
  console.log("initial is: ",initial);
  const [showAlgos, setShowAlgos] = useState<AlgorithmItem[]>(initial);  
  const updateAlgorithms= (params)=>
    queryAlgorithms(params).then((values)=>{
      values.data;//返回的算法数据
      //【】做类型检查与转换
      let temp:AlgorithmItem[]=[];
      for(let i in values.data)
        temp.push(values.data[i]);
      setShowAlgos(temp);
    });

  let showData=showAlgos;

  return(<>
  <Card gutter={0} layout="center" title="筛选搜索" bordered>
    <QueryFilter defaultCollapsed 
      onFinish={updateAlgorithms}
      onReset={updateAlgorithms}
      layout="vertical"
      defaultColsNumber={1}
      span={0}
      >
      <ProFormText name="name" width='xl' style={{ width: '100%' }} label="应用名称" />
      <ProFormSelect
        name="type"
        label="任务类型"
        mode="multiple"
        allowClear
        style={{ width: '50%' }}
        // placeholder="Please select"
        // defaultValue={['a10', 'c12']}
        request={
          async ()=>mission_type
        }
        onChange={handleChange}
      />
      <ProFormDateRangePicker name="dateRange" label="创建时间" />
      <ProFormText name="createUser" label="创建者" width="m"  
        //【】 待添加 输入后动态提示
      />

    </QueryFilter>
  </Card>
  <ProCard style={{ marginTop: 0 }} gutter={16} layout="center" title=""  >
    <List
      pagination={{
        defaultPageSize: 3,
        showSizeChanger: true,
      }}
      grid={{ gutter:16 , xs:1,
        sm:2, md:4, lg:4, xl:6,
        xxl:6,
      }}
      itemLayout="vertical"
      // loading={{
      //   delay:500,
      // }}
      dataSource={ showData }
      renderItem={(item) => (
        <List.Item>
          <Card title={item.name} bordered>
            {item.task}
            {item.createTime}
          </Card>
        </List.Item>
      )}
    />
  </ProCard>
  </>);
}
