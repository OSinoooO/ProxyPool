自建代理池，代码参考自《python3网络爬虫实战》——崔庆才。有所改动。  
运行需要搭建Flask、Redis环境  
各文件说明如下：  
  
Run——运行即可开启代理池，其中有Getter_module、Tester_module、proxyAPI_module三个模块的开关，可在代码中修改   
   
ProxyGet_module——代理获取模块，可增加代理网站接口（封装方法需以“crawl_”开头）  
  
Redis_module——数据库模块，包含一系列数据操作的方法   
  
Getter_module——连接代理获取模块和数据库模块，将获取的代理存入数据库   
  
Tester_module——代理检测模块，规则如下：获取到的代理赋初始值10分，每次用目标网址检测代理后，可用则立即赋值100分，不可用则减1分，分值小于0的代理则被移除    

proxyAPI_module——API接口模块，接口地址为：http://localhost:5000/random 。每次从Redis数据库中随机抽取一条可用代理。  
