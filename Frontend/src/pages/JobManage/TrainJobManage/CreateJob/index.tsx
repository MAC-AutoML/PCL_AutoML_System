import React, { useRef }  from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Alert, Typography, Radio,Cascader } from 'antd';
import ProCard from '@ant-design/pro-card';
import { PlusOutlined, SearchOutlined, EllipsisOutlined } from '@ant-design/icons';
import {message, Button, Tag, Space, Menu, Dropdown, Divider } from 'antd';
import ProForm, {
  StepsForm,
  ProFormText,
  ProFormDatePicker,
  ProFormSelect,
  ProFormTextArea,
  ProFormCheckbox,
  ProFormDateRangePicker,
  ProFormRadio,
  ProFormDigit,
} from '@ant-design/pro-form';import request from 'umi-request';
const waitTime = (time: number = 100) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
};
export default (): React.ReactNode =>{
  const radioStyle = {
    display: 'block',
    height: '30px',
    lineHeight: '30px',
  };
  const frame_cascaders=[
    {
      value: 'tensorflow',
      label: 'TensorFlow',
      children:[
        {
          value:'1.2',
          label:'1.2',
        },
        {
          value:'2.0',
          label:'2.0',
        },
      ]
    },
    {
      value: 'pytorch',
      label: 'Pytorch',
      children:[
        {
          value:'0.8',
          label:'0.8',
        },
        {
          value:'1.6',
          label:'1.6',
        },
      ]
    },
  ]
  const onchanger= (e)=>(console.log(e))

  const [dataType,setType]=React.useState(1)
  let algo_select;
  switch(dataType)
  {
    case 1:{
      algo_select=(<>
        <ProFormText
            width="m"
            name="algo_name"
            label="算法名称"
            tooltip="最长为 24 位"
            placeholder="请输入名称"
            rules={[{ required: true }]}        
        />
        <ProForm.Group title="调优参数">
          <Button >添加调优参数</Button>
          {/* 这里可以动态增加参数 */}
        </ProForm.Group >
        <ProForm.Group >
          <ProFormText 
            width="l"
            name="log_path"
            label="作业日志路径"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
        </ProForm.Group>

      </>)
      break;
    };
    case 2:{
      algo_select=(
      <ProForm.Group>
        <ProForm.Group title="AI引擎">
          <Cascader
            name='AI_driver'
            options={frame_cascaders}
            // defaultValue={['tensorflow','1.2']}
            // onChange={onchanger}
          />
        </ProForm.Group>
        <br />
        <ProForm.Group>
          <ProFormText 
            width="l"
            name="code_path"
            label="代码目录"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
          <ProFormText 
            width="l"
            name="start_file"
            label="启动文件"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
          <ProFormText 
            width="l"
            name="data_source"
            label="数据集来源"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
          <ProFormText 
            width="l"
            name="output_dir"
            label="训练输出位置"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
          <ProFormText 
            width="l"
            name="log_path"
            label="作业日志路径"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>

        </ProForm.Group>
      </ProForm.Group>)
      break;
    };
    case 3:{
      algo_select=(<>
        <ProForm.Group >
          <ProFormText 
            width="l"
            name="image_path"
            label="镜像地址"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>
          <ProFormText 
            width="l"
            name="code_path"
            label="代码目录"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>  
          <ProFormText 
            width="l"
            name="runner"
            label="运行命令"
          />
          <ProFormText 
            width="l"
            name="data_path"
            label="数据集合来源"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>         
          <ProFormText 
            width="l"
            name="output_dir"
            label="训练输出位置"
            placeholder="请点击右侧‘选择’按钮选择路径"
            disabled
          />
          <Button>选择</Button>
          <Button>清除</Button>     
          <ProForm.Group title="环境变量">
            <ProFormRadio.Button >添加环境变量</ProFormRadio.Button>
            {/* 这里可以动态增加参数 */}
            <br />
          </ProForm.Group >  
          <ProForm.Group>
            <ProFormText 
              width="l"
              name="log_path"
              label="作业日志路径"
              placeholder="请点击右侧‘选择’按钮选择路径"
              disabled
            />
            <Button>选择</Button>
            <Button>清除</Button>            
          </ProForm.Group>            
        </ProForm.Group>
        </>)
      break;
    };
  }

  return (
    <PageContainer>
      <ProCard >
        <StepsForm
          //此处为表单填写完成后的动作
          onFinish={async (values) => {
            console.log(values);
            await waitTime(1000);
            message.success('提交成功！');
          }}
          formProps={{
            validateMessages: {
              required: '此项为必填项',
            },
          }}
        >
          <StepsForm.StepForm
            name="base"
            title="服务选型"
            onFinish={async () => {
              await waitTime(100);
              return true;
            }}
          >
            <ProFormText
              name="name"
              label="实验名称"
              width="m"
              tooltip="最长为 24 位，用于标定的唯一 id"
              placeholder="请输入名称"
              rules={[{ required: true }]}
            />
            <ProFormTextArea
              name="description"
              label="描述"
              colSize={3}
              width="l"
            />   
            <Divider/>
            <Radio.Group
              value={dataType}
              onChange={(e) => setType(e.target.value)}
            >
              <Radio.Button value={1}>算法管理</Radio.Button>
              <Radio.Button value={2}>常用框架</Radio.Button>
              <Radio.Button value={3}>自定义</Radio.Button>
            </Radio.Group>    
            <br />          
            {algo_select}

            <Divider/>
            <Radio.Group>
              <Radio.Button> 公共资源池 </Radio.Button>
              <Radio.Button> 专属资源池 </Radio.Button>
            </Radio.Group>

            <br />
            <Radio.Group onChange={()=>(1)} value={Number}>
            <Radio style={radioStyle} value={1}> 算力资源配置1(待修改为根据后台信息动态配置) </Radio>
            <Radio style={radioStyle} value={2}> 算力资源配置2(待修改为根据后台信息动态配置) </Radio>
            <Radio style={radioStyle} value={3}> 算力资源配置3(待修改为根据后台信息动态配置) </Radio>
            </Radio.Group>
            <ProFormDigit 
              name="compute_node"
              label="计算节点个数"
              labelAlign="left"
              initialValue={1}
              min={1}
              max={8}
              fieldProps={{ precision: 0 }}
              //如何设置label与框在同一行
              // style={{float:"inline-start"}}
            />

          </StepsForm.StepForm>
          <StepsForm.StepForm name="checkbox" title="规格确认">
            <ProFormCheckbox.Group
              name="checkbox"
              label="迁移类型"
              width="l"
              options={['结构迁移', '全量迁移', '增量迁移', '全量校验']}
            />
            <ProForm.Group>
              <ProFormText name="dbname" label="业务 DB 用户名" />
              <ProFormDatePicker name="datetime" label="记录保存时间" width="s" />
              <ProFormCheckbox.Group
                name="checkbox"
                label="迁移类型"
                options={['完整 LOB', '不同步 LOB', '受限制 LOB']}
              />
            </ProForm.Group>
          </StepsForm.StepForm>
          <StepsForm.StepForm name="time" title="完成">
            <ProFormCheckbox.Group
              name="checkbox"
              label="部署单元"
              rules={[
                {
                  required: true,
                },
              ]}
              options={['部署单元1', '部署单元2', '部署单元3']}
            />
            <ProFormSelect
              label="部署分组策略"
              name="remark"
              rules={[
                {
                  required: true,
                },
              ]}
              initialValue="1"
              options={[
                {
                  value: '1',
                  label: '策略一',
                },
                { value: '2', label: '策略二' },
              ]}
            />
            <ProFormSelect
              label="Pod 调度策略"
              name="remark2"
              initialValue="2"
              options={[
                {
                  value: '1',
                  label: '策略一',
                },
                { value: '2', label: '策略二' },
              ]}
            />
          </StepsForm.StepForm>
        </StepsForm>
      </ProCard>
    </PageContainer>
  );
  
} 
