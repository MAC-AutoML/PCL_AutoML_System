# PCL_AutoML_System开发文档

## 一、文件夹功能分布

#### 1.总览

目前PCL_AutoML_System包含有algorithm，AutoML_Web,BBO,Frontend`四大文件模块`。

* algorithm：文件夹中存放基础深度学习算法。

* AutoML_Web：文件夹中存放后端代码和运行文件，包括数据库和API等。
* BBO：文件夹中存放黑盒优化算法。
* Frontend：文件夹中存放ant design pro前端代码和运行文件。

#### 2.algorithm

目录下存放基础深度学习代码，一级目录按任务类型划分，例如classification，detection。二级目录按算法类型划分，如ResNet,Vgg。

```
algorithm
|
|————classifcation
|	 |	
|    |——ResNet
|	 |
|    |——Vgg
|
|————detection
|	 |	
|    |——YOLO
|	 |
|    |——FasterRCNN
|
...
```

开发时需要按照目录树格式存放即可

#### 3.AutoML_Web

目录下存放后台代码及运行文件。后台代码框架使用python-django框架。django框架只使用后台部分，前台内容部分不需要进行变动。框架的主体代码文件有urls.py，view.py，models.py，API_tools.py。



- ##### models.py

models.py中存放数据库table代码，若有修改，需要依次运行：

`python manage.py makemigrations`
`python manage.py migrate`

即可修改项目所在服务器的数据库内容。

* ##### urls.py

AutoML_Web/urls.py中放前后台连接路由内容。通过在urlpatterns设置对应关系，前台的url路径与views.py中的内容相建立对应响应关系。

- ##### view.py

backend/view.py中存放后台逻辑相关内容，当django运行时，前台页面通过url路由调用view中class，通过APIView库，由前台的不同访问数据类型（post,get等），执行相应的代码。

- ##### API_tools.py

tools/API_tools.py中存放云脑接口封装代码，通过调用里面的函数，可以访问云脑对应功能。云脑API链接：http://192.168.202.71/rest-server/public/swagger-apidoc.yaml（http://192.168.202.73/swagger/ui/#/job/listJobs中输入链接）

#### 4、BBO

BBO文件夹中存放黑盒优化相关算法，将不同算法放入不同文件夹即可。

#### 5、Frontend

Frontend中存放前台代码，详见文件夹内readme.



## 二、部署

鹏程服务器挂载代码：

`sudo mount -t nfs 192.168.202.159:/mnt/neuronfs/ghome/wudch/ /wdc_mnt/`

#### 1. 后端部署

后端位于鹏程服务器挂载的位置，`cd wdc_mnt/PCL_AutoML`可进入。

进入项目文件夹后，进入后台文件夹`cd PCL_AutoML_System/AutoML_Web` ，运行代码

`python manage.py runserver http://127.0.0.1:8999/`可启动服务器。

若需要后台运行：

`nohup python manage.py runserver 192.168.207.73:8000 &`
### 2. 前端部署
前端基于[Ant Design Pro](https://pro.ant.design)开发。
前端同样位于项目文件夹 `cd wdc_mnt/PCL_AutoML`进入。
进入项目文件夹后，进入前端项目文件夹`cd PCL_AutoML_System/Frontend`
#### 前端运行环境

需要安装[node.js](https://nodejs.org/en/)

- node.js 12.19.0 / 14.15.1

#### 安装运行所需的js包

第一次启动前运行如下命令

```shell
npm install
```

#### 前端测试版服务器启动
**注意**需要开启后端服务器才能获取数据

```shell
npm run start:no-mock
```

#### 编译前端项目

```shell
npm run build
```
编译后的结果存放在项目根目录下的dist/文件夹
### 


