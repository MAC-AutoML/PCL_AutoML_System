import React, { useRef } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProCard from '@ant-design/pro-card'
import {Typography } from 'antd';
import styles from './index.less';
import {Link} from 'umi';

import { PlusOutlined, EllipsisOutlined } from '@ant-design/icons';
import { Button, Tag, Space, Menu, Dropdown } from 'antd';
import ProTable, { TableDropdown } from '@ant-design/pro-table';
import request from 'umi-request';

import shower from '../../../public/banner1.jpg'

const columns = [
  // {
  //   dataIndex: 'index',
  //   valueType: 'indexBorder',
  //   width: 48,
  // },
  {
    title: '项目名称',
    dataIndex: 'title', //回传数据的键
    // copyable: true,
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
    defaultSortOrder: 'descend',
    sorter: (a, b) => a > b, //使用何种排序
    render: (_) => <a>{_}</a>,
  },
  {
    title: '项目类型',
    dataIndex: 'state',
    initialValue: '图像分类',
    filters: true,
    valueType:'select',
    valueEnum: {
      all: {
        text: '全部',
        status: 'Default',
      },
      image_classification: {
        text: '图像分类',
        status: 'IC',
      },
      object_detection: {
        text: '物体检测',
        status: 'OD',
      },
      predict_analysis: {
        text: '预测分析',
        status: 'PA',
      },
    },
  },
  {
    title: '训练状态',//列表列名
    key: 'status',//未知
    dataIndex: 'train_status',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '部署状态',//列表列名
    key: 'status',//未知
    dataIndex: 'deploy_status',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '数据源',//列表列名
    key: 'status',//未知
    dataIndex: 'data_source',//回传的数据键名
    valueType: 'text',//未知 数据类型？
    defaultSortOrder: 'descend',
    sorter: (a, b) => a.age - b.age,
  },
  {
    title: '创建时间',
    key: 'since',
    dataIndex: 'created_at',
    valueType: 'date',
    defaultSortOrder: 'descend',
    sorter: (a, b) => a.age - b.age,
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
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="link">
        删除
      </a>,
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        查看
      </a>,
    ],
  },
];

export default (): React.ReactNode => {
  const actionRef = useRef();
  return (
    <PageContainer>
      <ProCard style={{ marginTop: 8 }} gutter={8} layout="center" title="" bordered headerBordered>
        <ProCard colSpan="auto" layout="center" bordered>    
          <Link to="/CreateMission?id=Image Classfiction">
            图像分类
          </Link>
        </ProCard>
        <ProCard colSpan="auto" layout="center" bordered>
          <Link to="/CreateMission?id=Image Classfiction">
          物体检测
          </Link>
        </ProCard>
        
        <ProCard colSpan="auto" layout="center" bordered>    
          <Link to="/CreateMission?id=Image Classfiction">
            预测分析
          </Link>
        </ProCard>
        
        <ProCard colSpan="auto" layout="center" bordered>
          <Link to="/CreateMission?id=Image Classfiction">
            声音分类
          </Link>    
        </ProCard>
        
        <ProCard colSpan="auto" layout="center" bordered>    
          <Link to="/CreateMission?id=Image Classfiction">
          文本分类
          </Link>
        </ProCard>
        
      </ProCard>
      <ProCard gutter={8} title="任务列表" layout="center" bordered headerBordered>
        <ProTable
        columns={columns}
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
        toolBarRender={() => [
          <Button key="button" icon={<PlusOutlined />} type="primary">
            新建
          </Button>,
        ]}
      />        
      </ProCard>
    </PageContainer>
  );
}