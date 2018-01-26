#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 配置请求执行完逻辑之后自动提交
SQLALCHEMY_COMMIT_ON_TEARDOWN = False
# 是否需要追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 启用记录查询统计数字的功能。
SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_DATABASE_URI = "postgresql://devusr:engine@localhost/mydb"
