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
  {
    dataIndex: 'index',
    valueType: 'indexBorder',
    width: 48,
  },
  {
    title: '标题',
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
  },
  {
    title: '状态',
    dataIndex: 'state',
    initialValue: 'open',
    filters: true,
    valueEnum: {
      all: {
        text: '全部',
        status: 'Default',
      },
      open: {
        text: '未解决',
        status: 'Error',
      },
      closed: {
        text: '已解决',
        status: 'Success',
      },
      processing: {
        text: '解决中',
        status: 'Processing',
      },
    },
  },
  {
    title: '标签',
    dataIndex: 'labels',
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
    title: '创建时间',
    key: 'since',
    dataIndex: 'created_at',
    valueType: 'date',
  },
  {
    title: '操作',
    valueType: 'option',
    render: (text, row, _, action) => [
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="link">
        链路
      </a>,
      <a href={row.url} target="_blank" rel="noopener noreferrer" key="view">
        查看
      </a>,
      <TableDropdown
        key="actionGroup"
        onSelect={() => action.reload()}
        menus={[
          {
            key: 'copy',
            name: '复制',
          },
          {
            key: 'delete',
            name: '删除',
          },
        ]}
      />,
    ],
  },
];
const menu = (
  <Menu>
    <Menu.Item key="1">1st item</Menu.Item>
    <Menu.Item key="2">2nd item</Menu.Item>
    <Menu.Item key="3">3rd item</Menu.Item>
    <Menu.Item key="4">4th item</Menu.Item>
  </Menu>
);

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
          <Dropdown key="menu" overlay={menu}>
            <Button>
              <EllipsisOutlined />
            </Button>
          </Dropdown>,
        ]}
      />        
      </ProCard>
    </PageContainer>
  );
}