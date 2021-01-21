import React, { useRef }  from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Alert, Typography } from 'antd';
import ProCard from '@ant-design/pro-card';
import { PlusOutlined, SearchOutlined, EllipsisOutlined } from '@ant-design/icons';
import { Button, Tag, Space, Menu, Dropdown } from 'antd';
import ProTable, { TableDropdown } from '@ant-design/pro-table';
import request from 'umi-request';

const my_algo = [
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
    title: '标签',//列表列名
    key: 'label',//未知
    dataIndex: 'label',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '版本',//列表列名
    key: 'version',//未知
    dataIndex: 'version',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '状态',//列表列名
    key: 'status',//未知
    dataIndex: 'status',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '大小',//列表列名
    key: 'model_size',//未知
    dataIndex: 'model_size',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '描述',//列表列名
    key: 'description',//未知
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
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="link">
        查看
      </a>,
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        删除
      </a>,
    ],
  },
];
const market_assign = [
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
    key: 'label',//未知
    dataIndex: 'label',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '版本数量',//列表列名
    key: 'version',//未知
    dataIndex: 'version',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '标签',//列表列名
    key: 'label',//未知
    dataIndex: 'label',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '可用时间',//列表列名
    key: 'useble_time',//未知
    dataIndex: 'useble_time',//回传的数据键名
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
    key: 'description',//未知
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

export default (props): React.ReactNode =>{
  const actionRef = useRef();
  return (
    <PageContainer>
      <ProCard
        tabs={{
          type: 'card',
        }}
      >
        <ProCard.TabPane key="my_algo" tab="我的算法">
          <ProTable
            columns={my_algo}
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
              <Button key="button" icon={<PlusOutlined />} type="primary"
              onClick={()=>{props.history.push("/AlgoManage/CreateAlgo");}}
              >
                新建
              </Button>,
            ]}
          />
        </ProCard.TabPane>
        <ProCard.TabPane key="assign_algo" tab="市场订阅">
          <ProTable
            columns={market_assign}
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
