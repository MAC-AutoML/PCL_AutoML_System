import React, { useRef }  from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { Card, Alert, Typography } from 'antd';
import ProCard from '@ant-design/pro-card';
import { PlusOutlined, SearchOutlined, EllipsisOutlined } from '@ant-design/icons';
import { Button, Tag, Space, Menu, Dropdown } from 'antd';
import ProTable, { TableDropdown } from '@ant-design/pro-table';
import request from 'umi-request';
import NoFoundPage from '@/pages/404';
import { queryMission} from './service';

const color_map={
  stopped: "default",
  failed:"error",
  running:"processing",
  succeeded:"success",
  waiting:"warning",
}
const columns = [
  {
    title: '任务名',
    dataIndex: 'name', //回传数据的键
    // copyable: true,
    ellipsis: true,
    tip: '标题过长会自动收缩',
    // width: '30%',
    search: false,
    defaultSortOrder: 'descend',
    // sorter: (a, b) => a > b, //使用何种排序
    // render: (dom, entity) => {
    //   return <a onClick={() => setRow(entity)}>{dom}</a>;
    // },  
  },
  {
    title: '状态',
    dataIndex: 'status',
    filters: true,
    valueType:'select',
    valueEnum: {
      stopped: {
        text: '停止',
        color: 'default',
        status: 'stopped',
      },
      failed: {
        text: '失败',
        color: 'error',
        status: 'failed',
      },
      running: {
        text: '运行中',
        color: 'processing',
        status: 'running',
      },
      succeeded: {
        text: '成功',
        color: 'success',
        status: 'succeeded',
      },
      waiting: {
        text: '等待中',
        color: 'warning',
        status: 'waiting',
      }},
      render: (dom, row,index,action) =>
        {
          // console.log(dom.props.valueEnum[row.status]);
          // console.log("ROW Contains:",row);
          // console.log("DOM Contains:",dom);
          // console.log("INDEX :",index);
          // console.log("ACTION :",action);
          return(
          // <Space>
            <Tag color={color_map[row.status]}>
            {dom.props.valueEnum[row.status].text}
            </Tag>
          // </Space>
          )},
  },
  {
    title: '创建时间',
    // key: 'since',
    dataIndex: 'created_at',
    valueType: 'date',
    defaultSortOrder: 'descend',
    // sorter: (a, b) => a > b,
  },
  {
    title: '结束时间',
    // key: 'since',
    dataIndex: 'completed_at',
    valueType: 'date',
    defaultSortOrder: 'descend',
    // sorter: (a, b) => a > b,
  },
  {
    title: '操作',
    valueType: 'option',
    render: (text, row, _, action) => [
      <Button danger key={1}> 删除 </Button>,
      <Button key={2}       > 查看 </Button>, 
    ],
  },
];

export default (props): React.ReactNode =>{
  const actionRef = useRef();
  return (
    <PageContainer>
      <ProCard >
        <ProTable
          columns={columns}
          actionRef={actionRef}
          request={(params, sorter, filter) => 
            queryMission({ ...params, sorter, filter })}
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
              onClick={()=>{props.history.push("/JobManage/TrainJobManage/CreateJob");}}
            >
              新建
            </Button>,
          ]}
        />
      </ProCard>
    </PageContainer>
  );
  
} 
