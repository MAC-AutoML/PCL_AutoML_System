import React, { useRef }  from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import { message } from 'antd';
import ProCard from '@ant-design/pro-card';
import { PlusOutlined, SearchOutlined, EllipsisOutlined, ConsoleSqlOutlined } from '@ant-design/icons';
import { Button, Tag, Space, Menu, Dropdown, Popconfirm } from 'antd';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';
import request from 'umi-request';

import { queryMission, deleteMission} from './service';
import {TableItem, TableListParams} from './data';
import { stringify } from 'qs';

const my_algo:ProColumns<TableItem>[] = [
  {
    title: '名称',
    dataIndex: 'name',
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
    title: '版本',//列表列名
    dataIndex: 'version',//回传的数据键名
    valueType: 'text',//未知 数据类型？
  },
  {
    title: '描述',//列表列名
    dataIndex: 'description',//回传的数据键名
    valueType: 'text',//未知 数据类型？
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
      <Popconfirm
        key="0"
        title="是否删除该项？"
        trigger="click"
        onConfirm={(_) =>{
          // action?.startEditable(row.key);
          let promise=deleteMission(row);
          let rep={};
          promise.then(
            (resp)=>{
              console.log("RESPONSE is: ",resp.data);
              rep=resp.data;
              return resp;}
          );
					// let infos:string=rep["reason"]
          if(!rep["success"] || rep["success"]==="false")
					{
						message.error('删除失败',3);
						message.error('该算法不存在，请刷新列表',3);
					}
          else
						message.success('删除成功',3);
				action.reload();
          // 删除失败怎么写
        }}
      >
        <Button danger key="1"> 删除 </Button>        
      </Popconfirm>,
      <Button key="2"> 查看 </Button> 
    ],
    // [
    //   <a href={row.url} target="_blank" rel="noopener noreferrer" key="link">
    //     查看
    //   </a>,
    // ],
  },
];

export default (props): React.ReactNode =>{
  const actionRef = useRef<ActionType>();
  return (
    <PageContainer>
      <ProCard >
        <ProTable
          columns={my_algo}
          actionRef={actionRef}
          request={(params, sorter, filter) => 
            queryMission({ ...params, sorter, filter })
          }
          rowKey="id"
          search={{
            labelWidth: 'auto',
          }}
          pagination={{
            pageSize: 10,
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
      </ProCard>
    </PageContainer>
  );
  
} 
