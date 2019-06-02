# Mongo_API
[![Build Status](https://travis-ci.org/flask-restful/flask-restful.svg?branch=master)](http://travis-ci.org/flask-restful/flask-restful)
[![Coverage Status](http://img.shields.io/coveralls/flask-restful/flask-restful/master.svg)](https://coveralls.io/r/flask-restful/flask-restful)
[![PyPI Version](http://img.shields.io/pypi/v/Flask-RESTful.svg)](https://pypi.python.org/pypi/Flask-RESTful)

Flask封装对MongoDB的增删改差

公司前技术总监把MongDB利用成了关系数据库，严格按照三范式建库，怎么理解三范式呢，就是普通的解析数据全部转化成了实体关系，分为meta表和data表，我真的很膜拜。

然而他走了，调用的接口我来写，这就真的很蓝首...

具体mongoDB里就有这两个数据库
**data 实体关系属性**
![m1](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo1.png)
**meta 实体关系属性**
![m2](https://github.com/fenglei110/Mongo_API/blob/master/images/mongo2.png)

具体rest api接口，对MongoDB的增删改查看下面：

[API文档](images/demo_api.pdf)

因为匆匆部署，没有添加详细使用文档，谅解。