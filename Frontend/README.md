# PCL自动机器学习平台-前端项目文档

前端项目基于Ant Design Pro v5进行开发。

本文假设读者已经具有基本的前端开发能力，比较了解HTML/CSS/Javascript等基本知识，基本入门React前端框架。

## 在开始之前

#### 关于Ant Design与Ant Design Pro

首先我们需要对Ant Design Pro (下文简称Antd-pro) 有一定的了解：

以下这段介绍来自antd-pro的[官网文档](https://pro.ant.design/docs/getting-started-cn)

> Ant Design Pro 是一个企业级中后台前端/设计解决方案，我们秉承 [Ant Design](http://ant.design/) 的设计价值观，致力于在设计规范和基础组件的基础上，继续向上构建，提炼出典型模板/业务组件/配套设计资源，进一步提升企业级中后台产品设计研发过程中的『用户』和『设计者』的体验。随着『设计者』的不断反馈，我们将持续迭代，逐步沉淀和总结出更多设计模式和相应的代码实现，阐述中后台产品模板/组件/业务场景的最佳实践，也十分期待你的参与和共建。

这里提到了[Ant Design](https://ant.design/index-cn) (下文简称antd)，初次接触的人可能会弄不清antd和antd-pro的关系，这里我来详细解释下。

antd是一套由蚂蚁集团体验技术部开发的设计规范。

> 随着商业化的趋势，越来越多的企业级产品对更好的用户体验有了进一步的要求。带着这样的一个终极目标，我们（蚂蚁集团体验技术部）经过大量项目实践和总结，逐步打磨出一个服务于企业级产品的设计体系 —— Ant Design。

既然是一套规范，那么在运用到项目中时，就需要具体的代码实现。因此antd还提供了基于react前端框架的实现：[Ant Design of React - Ant Design](https://ant.design/docs/react/introduce-cn) 。

antd-pro便是基于antd of react 实现的**更高层级的前端手脚架**(提供前端项目模板)。

antd-pro开发组还提供了一些"组件即页面"的重型组件：[ProComponents](https://procomponents.ant.design/) 。

## 项目结构介绍

项目结构如下：

```shell
.
├── AddNewPages.md
├── archive/
├── config/ # # 设置文件夹,包括外观、路由、代理等项目基本设置
├── jest.config.js
├── jsconfig.json
├── mock/ # # 模拟数据文件夹，内含生成模拟数据的文件
├── node_modules/ # # nodejs 包文件夹
├── package.json # # nodejs项目命令和依赖
├── package-lock.json
├── public/ # # 静态公共资源文件夹
├── README.md
├── src/ # # 源代码文件夹，页面等放置于此
├── tests/ # # 测试代码文件夹
└── tsconfig.json
```

重点要熟悉以下几个文件夹:

```shell
config/ 	# # 设置文件夹,包括外观、路由、代理等项目基本设置
mock/ 		# # 模拟数据文件夹，内含生成模拟数据的文件
public/		# # 静态公共资源文件夹
src/		# # 源代码文件夹，页面等放置于此
```

#### config文件夹:

结构如下：

```shell
.
├── config.ts 			# # 设置文件 - 主文件
├── defaultSettings.ts 	# # 默认设置,主要是关于外观风格等的设置
├── proxy.ts 			# # 转发代理设置
└── routes.ts 			# # 路由文件
```

#### src文件夹:

结构如下:

```shell
.
├── access.ts
├── app.tsx
├── components/ 		# # 可复用组件代码文件夹
├── e2e/
├── global.less
├── global.tsx
├── locales/ 			# # 国际化/多语种翻译 文件夹
├── manifest.json
├── pages/ 				# # 页面文件夹 # # 最常用
├── services/ 			# # 与后端数据交互函数 文件夹
├── service-worker.js
├── typings.d.ts
└── utils/
```

我们约定，项目中每个功能页面/页面组都以单个文件夹的形式放置在"pages"文件夹中。

页面组：指一个单项功能及其包含的子页面，比如："自动机器学习"功能包括"当前任务列表与新建任务入口"页面和"创建新任务"页面。



## 如何添加新页面

我们以一个例子来说明如何创建新页面。

假设我们要添加一个名为”创建模型“的新页面。

1. ### 创建新页面的文件

   由前述文档我们知道，项目中的每个页面/页面组都在“./src/pages”下以单独的文件夹形式进行组织，如:

   ```shell
   .
   ├── 404.tsx
   ├── Admin.tsx
   ├── AIMarket/
   ├── AutoML/
   ...
   ├── user/
   ├── Welcome.less
   └── Welcome.tsx
   ```

   我们约定，每个页面/页面组文件夹下的文件按如下结构组织，以AutoML页面组为例：

   ```
   .
   ├── CreateMission/
   │   ├── components.tsx
   │   ├── data.d.ts
   │   ├── index.less
   │   ├── index.tsx
   │   └── service.ts
   └── ListMission/
       ├── components.tsx
       ├── data.d.ts
       ├── index.less
       ├── index.tsx
       └── service.ts
   ```

   这里AutoML组下有两个子页面，分别承担罗列当前任务、创建新任务的功能。可以看到，两个子页面下的文件名相同，包括以下几个文件：

   ```shell
   index.tsx # 主要文件，构造页面的文件，被React引擎解析后生成页面
   index.less # 页面CSS文件
   service.ts # 页面与后端交互函数的文件
   component.tsx # 页面组件功能代码的文件
   data.d.ts # 定义页面所用数据结构/接口结构的文件
   ```

   > **注意**：这五个文件名是我们为了统一格式，方便开发和阅读而约定的文件名，不是必须要这样做。

   我们创建一个名为"ListModel"的新文件夹，并在该文件夹内创建以上五个文件。

2. ### 编写具体代码

   推荐先浏览其他页面的文件。

   推荐"index.tsx"中默认default函数返回"React.ReactNode"类型：

   ```typescript
   export default (): React.ReactNode => {
       //...
       //status等代码
       //...
       return (
           <>
           //页面组件 
           </>
       );
   }
   ```

   

3. ### 在路由中添加新路径

   由前述文档可知，项目的路由文件是"./config/routes.ts"。那么我们要在该文件里仿照其他页面的路由设置，来添加ListModel的设置：

   ```typescript
     {
       path: '/ListModel', // url路径
       name: '模型列表', //在页面/菜单中显示的标题
       icon: 'smile', //在菜单中显示时的图标
       component: './ListModel', //页面组件的存放路径，当构造页面的文件命名为'index.tsx'时，框架会自动解析。
       // hideInMenu: 'true',  //为 true 则在页面左侧菜单中隐藏
     },
   ```

   至此新页面添加完毕，可以打开浏览器进行debug了。

## 必备资源

- V5 链接：[Ant Design Pro - 开箱即用的中台前端/设计解决方案](https://beta-pro.ant.design/index-cn)
- V4 链接： [开始使用 - Ant Design Pro](https://pro.ant.design/docs/getting-started-cn)
- Pro重型组件：[ProComponents - 页面级别的前端组件 (ant.design)](https://procomponents.ant.design/)
- 重型组件组件Github项目地址：[ant-design/pro-components (github.com)](https://github.com/ant-design/pro-components/blob/master/docs/index.md)
- V2基础部件库：[用户头像列表 AvatarList - Ant Design](https://v2-pro.ant.design/components/avatar-list-cn)
- 如何单独使用部件：[独立使用 Pro 组件 - Ant Design](https://v2-pro.ant.design/docs/use-components-alone-cn)
- Ant Design 组件总览： [组件总览 - Ant Design](https://ant.design/components/overview-cn/)

这里需要稍微解释下：因为antd-pro目前(2020.12)已经开发了五个版本，每个版本都或多或少的基于上个版本开发的组件库，因此在我们本项目的开发中，时常需要参考’组件总览‘等资源。
