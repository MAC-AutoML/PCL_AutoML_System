﻿export default [
  //设计的页面
  //level:01, id:01 
  {
    path: '/OverView',
    name: '总览',
    icon: 'smile',
    component: './OverView',
    // hideInMenu: 'true', 
  },  
  //level:01, id:02 
  {
    path: '/AutoML',
    name: '自动学习',
    icon: 'smile',
    component: './AutoML',
    // hideInMenu: 'true', 
  },
  //level:01 id 021
  {
    path:'/CreateMission',
    name:'创建任务',
    icon:'torch',
    component:'./CreateMission',
    hideInMenu:'true',
  },
  //level:01, id:03 
  {
    path: '/DataManage',
    name: '数据管理',
    icon: 'smile',
    component: './DataManage',
    // hideInMenu: 'true', 
  },
  //level:01, id:04 
  {
    path: '/DevEnv',
    name: '开发环境',
    icon: 'table',
    // component: './DevEnv',
    routes: [//子界面
      {
        path: '/DevEnv/JupyterNotebook',
        name: 'JupyterNotebook',
        icon: 'smile',
        component: './DevEnv/JupyterNotebook',
      },
    ]
    // hideInMenu: 'true', 
  },
  //level:01, id:05 
  {
    path: '/AlgoManage',
    name: '算法管理',
    icon: 'smile',
    component: './AlgoManage',
    // hideInMenu: 'true', 
  },
  //level:01, id:06 
  {
    path: '/JobManage',
    name: '作业管理',
    icon: 'table',
    // component: './JobManage',
    // hideInMenu: 'true', 
    routes: [//子界面
      {
        path: '/JobManage/TrainJobManage',
        name: '训练作业管理',
        icon: 'smile',
        component: './JobManage/TrainJobManage',
      },
      {
        path: '/JobManage/AutoJobManage',
        name: '自动搜索作业管理',
        icon: 'smile',
        component: './JobManage/AutoJobManage',
      },
    ]
  },
  //level:01, id:07 
  {
    path: '/ModelManage',
    name: '模型管理',
    icon: 'smile',
    component: './ModelManage',
    // hideInMenu: 'true', 
  },
  //level:01, id:08
  {
    path: '/AIMarket',
    name: 'AI市场',
    icon: 'smile',
    component: './AIMarket',
    // hideInMenu: 'true', 
  },
  //设计页面结束
  {
    path: '/user',
    layout: false,
    routes: [
      {
        name: 'login',
        path: '/user/login',
        component: './user/login',
      },
    ],
  },
  // {
  //   path: '/admin',
  //   name: 'admin',
  //   icon: 'crown',
  //   access: 'canAdmin',
  //   component: './Admin',
  //   routes: [
  //     {
  //       path: '/admin/sub-page',
  //       name: 'sub-page',
  //       icon: 'smile',
  //       component: './Welcome',
  //     },
  //   ],
  // },
  // {
  //   name: 'list.table-list',
  //   icon: 'table',
  //   path: '/list',
  //   component: './ListTableList',
  // },
  {
    path: '/',
    redirect: '/OverView',
  },
  
  {
    component: './404',
  },
];
