
*  对图书数据使用基于tensorflow的协同过滤算法

### 功能清单

```
注册，登录，检索查询，评分，推荐，购物车，书单，删除购物车，删除书单，收藏，取消收藏。
管理员权限： 删除用户，添加书籍，删除书籍。
```

## 所需运行环境

* 使用python3.6作为编程语言。使用mysql作为数据库存储.
* 需要安装pandas,flask，pymysql.
*　安装方式:
```
    pip install pandas
    pip install flask
    pip install pymysql
```

## 项目源码介绍

图书推荐系统
```
----Flask-BookRecommend-Mysql\
    |----data                         >这个文件夹中存放数据集，数据集比较杂乱。                    
    |----web\                        >web端 
    |    |----logger.py               >日志记录
    |    |----config.yml              >配置参数
    |    |----logs                    >日志
    |    |----app.py                  >web入口
    |    |----utils.py                >辅助模块
    |----CF_use_python.py            >协同过滤：CF 算法
    |----CF_use_tensorflow.py        >使用tensorflow实现的协同过滤CF算法
    |----read_data_save_to_mysql.py  >读取data文件夹里面的书籍存储到数据库中
    |----README.md
```

## 项目启动方式：
* 首先建立自己的mysql数据库
* 运行read_data_save_to_mysql.py文件 将数据导入到mysql中。
  注意mysql的链接参数.修改为自己的连接参数（id,code,端口）需要修改read_data_save_to_mysql和web/config.yml文件下的mysql的配置参数。
* 进入web文件夹,运行app.py
* 在浏览器上访问 127.0.0.1:8080
* 使用下载数据中的UserID和其对应的Location作为账号密码登录网站，或者自己注册登录。
* 系统管理员的账号：admin 密码：admin 通过这个账号密码进入后台管理
* example:
  + id：nyc
  + code: new york

## 项目功能：

本项目主要实现了3个图书推荐功能：
+ 热门书籍 
    + 是将评分排名最高的几本书推荐给用户
+ 猜你喜欢
    + 通过数据库SQL语句实现
    + ”看了这本书的人也看了XX书“
    + 主要逻辑是：
        + 首先查该用户的浏览记录
        + 通过浏览过的书籍，找到也看过这本书的人
        + 在也看过这本书的人中，找评分较高的书推荐给用户
+ 推荐书籍
    + 使用到了协同过滤算法，实现书籍的推荐

