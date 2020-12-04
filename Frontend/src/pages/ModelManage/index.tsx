import React, { useRef }  from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Alert, Typography } from 'antd';
import ProCard from '@ant-design/pro-card';
import { PlusOutlined, SearchOutlined, EllipsisOutlined } from '@ant-design/icons';
import { Button, Tag, Space, Menu, Dropdown } from 'antd';
import ProTable, { TableDropdown } from '@ant-design/pro-table';
import request from 'umi-request';

const t_manage = [
  {
    title: '名称',
    dataIndex: 'title',
    copyable: true,
    ellipsis: true,
    tip: '标题过长会自动收缩',
    formItemProps: {
      rules: [
        {
          required: true,
          message: '此项为必填项',
        },
      ],
    },
    width: '30%',
    search: false,
    sorter: (a, b) => a > b, //使用何种排序
    render: (_) => <a>{_}</a>,
  },
  {
    title: '最新版本',//列表列名
    key: 'status',//未知
    dataIndex: 'model_size',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '版本数量',//列表列名
    key: 'status',//未知
    dataIndex: 'version',//回传的数据键名
    valueType: 'text',//未知 数据类型？
    sorter: (a, b) => a > b, //使用何种排序
  },
  {
    title: '部署类型',
    dataIndex: 'labels',
    // dataIndex: 'state',
    initialValue: '全部',
    filters: true,
    valueType:'select',
    valueEnum: {
      all: {
        text: '全部',
        status: 'Default',
      },
      image_classification: {
        text: '失败',
        color: 'error',
        status: 'IC',
      },
      object_detection: {
        text: '运行中',
        color: 'default',
        status: 'OD',
      },
      predict_analysis: {
        text: '成功',
        color: 'success',
        status: 'PA',
      },
    },
    //渲染函数需要修改，例如：
    // render:(_,row) =>(
    //   <Space>
    //       <Tag color={row.labels.color} key={row.labels.text}>
    //         {row.labels.text}
    //       </Tag>
    //   </Space>      
    // )
    render: (_, row) => (
      <Space>
        {row.labels.map(({ name, color }) => (
          <Tag color={color} key={name}>
            {name}
          </Tag>
        ))}
      </Space>
    ),
  },
  {
    title: '描述',//列表列名
    key: 'status',//未知
    dataIndex: 'description',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '创建时间',
    key: 'since',
    dataIndex: 'created_at',
    valueType: 'date',
    sorter: (a, b) => a > b, //使用何种排序
  },
  {
    title: '操作',
    valueType: 'option',
    render: (text, row, _, action) => [
      //待添加功能：任务只有在运行状态下该按钮才可以点， button组件有属性可以设置为 disable
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="link" >
        停止
      </a>,
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        删除
      </a>,
    ],
  },
];
const p_manage = [
  {
    title: '名称',
    dataIndex: 'title',
    copyable: true,
    ellipsis: true,
    tip: '标题过长会自动收缩',
    formItemProps: {
      rules: [
        {
          required: true,
          message: '此项为必填项',
        },
      ],
    },
    width: '30%',
    search: false,
    sorter: (a, b) => a > b, //使用何种排序
    render: (_) => <a>{_}</a>,
  },
  {
    title: '引擎类型',//列表列名
    key: 'status',//未知
    dataIndex: 'label',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '订阅时间',
    key: 'since',
    dataIndex: 'created_at',
    valueType: 'date',
    sorter: (a, b) => a > b, //使用何种排序
  },
  {
    title: '描述',//列表列名
    key: 'status',//未知
    dataIndex: 'description',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '操作',
    valueType: 'option',
    render: (text, row, _, action) => [
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        查看
      </a>,
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        删除
      </a>,
    ],
  },
];

export default (): React.ReactNode =>{
  const actionRef = useRef();
  return (
    <PageContainer>
      <ProCard
        tabs={{
          type: 'card',
        }}
      >
        <ProCard.TabPane key="my_algo" tab="我的模型">
          <ProTable
            columns={t_manage}
            actionRef={actionRef}
            request={async (params = {}) =>
              request('https://proapi.azurewebsites.net/github/issues', {
                params,
              })
            }
            rowKey="id"
            search={{
              labelWidth: 'auto',
            }}
            pagination={{
              pageSize: 5,
            }}
            dateFormatter="string"
            // headerTitle="高级表格"
            toolBarRender={() => [
              <Button key="button" icon={<PlusOutlined />} type="primary left">
                新建模型
              </Button>,
              <Button key="button" icon={<SearchOutlined />} type="primary">
                查找模型
              </Button>,
            ]}
          />
        </ProCard.TabPane>
        <ProCard.TabPane key="assign_algo" tab="市场订阅模型">
          <ProTable
            columns={p_manage}
            actionRef={actionRef}
            request={async (params = {}) =>
              request('https://proapi.azurewebsites.net/github/issues', {
                params,
              })
            }
            rowKey="id"
            search={{
              labelWidth: 'auto',
            }}
            pagination={{
              pageSize: 5,
            }}
            dateFormatter="string"
            // headerTitle="高级表格"
            toolBarRender={() => [
              <Button key="button" icon={<SearchOutlined />} type="primary">
                查找算法
              </Button>,
            ]}
          />
        </ProCard.TabPane>
      </ProCard>
    </PageContainer>
  );
  
} 
