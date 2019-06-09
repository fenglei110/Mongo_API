# Mongo_API
[![Build Status](https://travis-ci.org/flask-restful/flask-restful.svg?branch=master)](http://travis-ci.org/flask-restful/flask-restful)
[![Coverage Status](http://img.shields.io/coveralls/flask-restful/flask-restful/master.svg)](https://coveralls.io/r/flask-restful/flask-restful)
[![PyPI Version](http://img.shields.io/pypi/v/Flask-RESTful.svg)](https://pypi.python.org/pypi/Flask-RESTful)

Flask封装对MongoDB的增删改差

公司前技术总监把MongDB利用成了关系数据库，严格按照三范式建库，怎么理解三范式呢，就是普通的解析数据全部转化成了实体关系，分为meta表和data表，我真的很膜拜。

然而他走了，调用的接口我来写，这就真的很蓝首...

**代码大致流程如下**
![M](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo流程.png)

具体mongoDB里存在这两个库：

**存储`meta`的实体，实体属性，关系，关系属性**

![m1](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo1.png)

**存储`data`的实体，关系，属性**

![m2](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo2.png)

**API web界面，虽然丑点。具体前端界面代码没有上传，可以调用api**

**为实体创建属性**

![m3](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo3.png)

**此代码所处理的数据就是天眼查爬来的公司信息以及工商信息，通过三范式转化成ER模型。**

**数据整理为json，查看目录[Data](Data)，记录了中国大陆 31 个省份1978 年至 2019 年
一千多万工商企业注册信息，包含企业名称、注册地址、统一社会信用代码、地区、注册日期、
经营范围、法人代表、注册资金、企业类型等详细资料。勿商用！**

![m4](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo4.png)

**增加关系**

![m5](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo5.png)

**增加实体**

![m6](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo6.png)

具体rest api接口，对MongoDB的增删改查请看文档：

[Flask调用MongDB增删改查的API文档](images/demo_api.pdf)

因为匆匆部署，没有添加详细使用文档，谅解。若需要，提issue。