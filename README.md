# 知乎日报网页版

基于Django的知乎日报的网页版，思路和大部分代码来源于[JobsDong/zhihudaily](https://github.com/JobsDong/zhihudaily)

## 项目结构

        ├── README.md               项目介绍
        ├── requirements.txt        项目依赖
        └── zhihudaily
            ├── config              项目配置
            ├── daily               日报APP
            ├── db.sqlite3
            ├── manage.py
            ├── media               存放日报封面，按日期分目录保存
            ├── static              静态资源，存放前端代码
            ├── templates           模板文件
            └── test
                └── insert_data.py  插入数据

## 实现说明

    代码其实很简单，后端用Django实现，Celery用于定时采集信息，每隔1小时检查一次
    前端页面通过Django模板输出，使用BootStrap和Jquery
    在我的电脑Arch Linux（Django 1.9.7 / Python 2.7.11）测试通过

## 安装与运行

* 安装依赖
```sh
    pip install -r requirements.txt
```

* 插入数据
```sh
    cd zhihudaily/test
    python insert_data.py
```
* 运行
```sh
    cd zhihudaily
    python manage.py runserver 9000
    celery -A config beat
    celery -A config worker --loglevel=info
```
