import React, { Children } from 'react';
import { Card, Typography, Alert, Button } from 'antd';
import { PageContainer } from '@ant-design/pro-layout';
import { message, Radio } from 'antd';
import ProForm, {
  LightFilter,
  ProFormText,
  ProFormTextArea,
  ProFormDatePicker,
  ProFormSelect,
  ProFormDigit,
  ProFormSwitch,
  ProFormDateRangePicker,
  ProFormDateTimePicker,
  ProFormTimePicker,
  ProFormSlider,
  } from '@ant-design/pro-form';
import Title from 'antd/lib/typography/Title';

const waitTime = (time = 100) =>
  new Promise(resolve => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
export default (props): React.ReactNode =>{
  const [dataType,setType]=React.useState(true)
  let dataSelect;
  if(dataType){
    dataSelect=(<>
      <ProFormText
        width="m"
        name="dataName"
        label="新数据集命名"
        tooltip="最长为 24 位"
        placeholder="请输入名称"
        rules={[{ required: true }]}
      />
      <ProFormText
        width="xl"
        name="dataOutput"
        label="数据集输入位置"
        tooltip="最长为 24 位"
        placeholder="请选择路径"
        rules={[{ required: true }]}
      />
      <ProFormText
        width="xl"
        name="dataInput"
        label="数据集输出位置"
        tooltip="最长为 24 位"
        placeholder="请选择路径"
        rules={[{ required: true }]}
      />
      </>
      )
  }
  else{
    dataSelect=(
      <ProFormText
        width="m"
        name="dataSelection"
        label="选择数据集"
        tooltip="最长为 24 位"
        placeholder="请输入名称"
        rules={[{ required: true }]}
      />)
  }

  return (
  <PageContainer content="" >
    <Card>
      <ProForm
      onFinish={async values => {
        await waitTime(2000);
        console.log(values);
        message.success('提交成功！');
      }}
      initialValues={{
        name: '',
        useMode: 'chapter',
      }}
      layout="vertical"
      >
        <ProForm.Group>
          <ProFormText
            width="m"
            name="name"
            label="名称"
            tooltip="最长为 24 位"
            placeholder="请输入名称"
            rules={[{ required: true }]}
          />
        </ProForm.Group>
        <ProForm.Group>
          <ProFormTextArea name="description" label="描述" width="l" placeholder="任务项目描述" />
        </ProForm.Group>
        <ProForm.Group >
          <Typography.Text strong>
          数据集来源
          </Typography.Text>
          <Radio.Group
              value={dataType}
              onChange={() => setType(!dataType)}
          >
            <Radio.Button value={true}>新建数据集</Radio.Button>
            <Radio.Button value={false}>已有数据集</Radio.Button>
          </Radio.Group>
        </ProForm.Group>
        <ProForm.Group >
          {dataSelect}
        </ProForm.Group>
        <ProForm.Group >
          <ProFormDigit 
              name="modelsize"
              label="最大FLOPS上限(单位：M)"
              tooltip="单位： M"
              rules={[{ required: true }]}
          />
        </ProForm.Group>        
      </ProForm>
    </Card>
  </PageContainer>
  )
};