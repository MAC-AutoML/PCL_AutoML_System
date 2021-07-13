export default [
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
    authority: ['admin', 'user'],
    // hideInMenu: 'true', 
    routes: [//子界面
      {
        path: '/AutoML',
        name: '自动学习任务列表',
        // icon: 'smile',
        component: './AutoML/ListMission',
        hideInMenu:'true',
        exact:true,
      },
      {
        path: '/AutoML/CreateMission/:type',
        name: '创建自动学习任务',
        icon: 'smile',
        component: './AutoML/CreateMission',
        hideInMenu:'true',
      },
    ]
  },
  //level:01 id 021
  // {
  //   path:'/CreateMission',
  //   name:'创建任务',
  //   icon:'torch',
  //   component:'./CreateMission',
  //   hideInMenu:'true',
  // },
  //level:01, id:03 
  // {
  //   path: '/DataManage',
  //   name: '数据集管理',
  //   icon: 'smile',
  //   component: './DataManage',
  //   authority: ['admin', 'user'],

  //   // hideInMenu: 'true', 
  // },
  //level:01, id:04 
  // {
  //   path: '/DevEnv',
  //   name: '开发环境',
  //   icon: 'table',
  //   authority: ['admin', 'user'],
  //   // component: './DevEnv',
  //   routes: [//子界面
  //     {
  //       path: '/DevEnv/JupyterNotebook',
  //       name: 'JupyterNotebook',
  //       icon: 'smile',
  //       component: './DevEnv/JupyterNotebook',
  //     },
  //   ]
  //   // hideInMenu: 'true', 
  // },
  //level:01, id:05 
  {
    path: '/AlgoManage',
    name: '算法管理',
    icon: 'smile',
    // component: './AlgoManage',
    authority: ['admin', 'user'],
    // hideInMenu: 'true', 
    routes:[
      {
        path:'/AlgoManage',
        // name:'算法列表',
        component:'./AlgoManage/ListAlgo',
        hideInMenu:'true',
        exact:true,
      },
      {
        path:'/AlgoManage/CreateAlgo',
        name:'创建算法',
        icon:'smile',
        component:'./AlgoManage/CreateAlgo',
        hideInMenu:true,
      },
    ]
  },
  //level:01, id:06 
  // {
  //   path: '/JobManage',
  //   name: '作业管理',
  //   icon: 'table',
  //   // component: './JobManage',
  //   authority: ['admin', 'user'],
  //   // hideInMenu: 'true', 
  //   routes: [//子界面
  //     {
  //       path: '/JobManage/TrainJobManage',
  //       name: '训练作业管理',
  //       icon: 'smile',
  //       // component: './JobManage/TrainJobManage',
  //       routes: [//子界面
  //         {
  //           path: '/JobManage/TrainJobManage',
  //           // name: '',
  //           icon: 'smile',
  //           component: './JobManage/TrainJobManage',
  //           hideInMenu: true, 
  //           exact:true,
  //         },
  //         {
  //           path: '/JobManage/TrainJobManage/CreateJob',
  //           name: '创建训练任务',
  //           icon: 'smile',
  //           component: './JobManage/TrainJobManage/CreateJob',
  //           hideInMenu: true, 
  //           // exact:true,
  //         },
  //       ],
  //     },
  //     {
  //       path: '/JobManage/AutoJobManage',
  //       name: '自动搜索作业管理',
  //       icon: 'smile',
  //       // component: './JobManage/AutoJobManage',
  //       routes: [//子界面
  //         {
  //           path: '/JobManage/AutoJobManage',
  //           // name: '',
  //           icon: 'smile',
  //           component: './JobManage/AutoJobManage',
  //           hideInMenu: true, 
  //           exact:true,
  //         },
  //         {
  //           path: '/JobManage/AutoJobManage/CreateJob',
  //           name: '创建训练任务',
  //           icon: 'smile',
  //           component: './JobManage/AutoJobManage/CreateJob',
  //           hideInMenu: true, 
  //           // exact:true,
  //         },
  //       ],
  //     },
  //   ]
  // },
  {
    path: '/JobManage/TrainJobManage',
    name: '训练作业管理',
    icon: 'smile',
    authority: ['admin', 'user'],
    // component: './JobManage/TrainJobManage',
    routes: [//子界面
      {
        path: '/JobManage/TrainJobManage',
        // name: '',
        icon: 'smile',
        component: './JobManage/TrainJobManage/ListJob',
        hideInMenu: true, 
        exact:true,
      },
      {
        path: '/JobManage/TrainJobManage/CreateJob',
        name: '创建训练任务',
        icon: 'smile',
        component: './JobManage/TrainJobManage/CreateJob',
        hideInMenu: true, 
        // exact:true,
      },
    ],
  },
  {
    path: '/JobManage/AutoJobManage',
    name: '自动搜索作业管理',
    icon: 'smile',
    authority: ['admin', 'user'],
    // component: './JobManage/AutoJobManage',
    routes: [//子界面
      {
        path: '/JobManage/AutoJobManage',
        // name: '',
        icon: 'smile',
        component: './JobManage/AutoJobManage/ListJob',
        hideInMenu: true, 
        exact:true,
      },
      {
        path: '/JobManage/AutoJobManage/CreateJob',
        name: '创建训练任务',
        icon: 'smile',
        component: './JobManage/AutoJobManage/CreateJob',
        hideInMenu: true, 
        // exact:true,
      },
    ],
  },
  //level:01, id:07 
  // {
  //   path: '/ModelManage',
  //   name: '模型管理',
  //   icon: 'smile',
  //   authority: ['admin', 'user'],
  //   component: './ModelManage',
  //   // hideInMenu: 'true', 
  // },
  // //level:01, id:08
  // {
  //   path: '/AIMarket',
  //   name: 'AI市场',
  //   icon: 'smile',
  //   authority: ['admin', 'user'],
  //   component: './AIMarket',
  //   //【】如何让菜单在该页面中默认收起
  //   // hideInMenu: 'true', 
  // },
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
