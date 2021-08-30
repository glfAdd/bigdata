# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zookeeper
kazoo库使用
"""
from kazoo.client import KazooClient
from kazoo.client import KazooState


# .........................................................监听的方法
def my_watch1(data, state):
    """监视器函数，得有一个形参，监视的节点或者子节点变化时被调用"""
    print "my_watch1:", data, state


def my_watch2(event):
    print "my_watch2:", event


# .........................................................连接zookeeper
# zk = KazooClient(hosts='127.0.0.1:2181')
# zk.start(timeout=45)
zk = KazooClient(hosts='127.0.0.1:2181', timeout=45)
zk.start()

# .........................................................状态
# LOST刚创建时  CONNECTED连接建立成功  SUSPENDED断开连接
print zk.state
print zk.connected
print zk.exists("/tests/zk1")
# .........................................................get set
# 获取详情, 并注册监视器函数
zk.set('/abc/JQK/XYZ/00020000000054', b'123123')
# version 必须是存在的
zk.set('/abc/JQK/XYZ/00020000000053', b'123123', version=21)
# watch 监听函数
print zk.get("/abc/JQK/XYZ/00020000000053", watch=my_watch1)
print zk.get_children("/abc", watch=my_watch2)
# 递归创建节点路径, 不添加数据
zk.ensure_path('/abc/JQK/XYZ/0003')
# makepath: True递归创建节点, False(默认)父节点必须存在, 节点如果存在报错
# sequence: 临时节点
zk.create('/abc/JQK/XYZ/0002', b'this is my house', makepath=True)
# True递归 无论是否为空都删除, Flase 如果不为空删除失败
zk.delete('/abc', recursive=True)


# .........................................................调用方法监听
def test_watch_data(event):
    print("this is a watcher for node data.")


zk.get_children("/china", watch=test_watch_data)


# .........................................................装饰器监听
# 当下一代子节点发生变化时触发
@zk.ChildrenWatch("/china")
def watch_china_children(children):
    print("this is watch_china_children %s" % children)


# 当节点数据发生变化时触发
def watch_china_node(data, state):
    print '%s--------%s' % (data, state)


# .........................................................监听客户端3种连接状态
# 相当于my_listener = zk.add_listener(my_listener)
@zk.add_listener
def my_listener(state):
    # 监听客户端3种连接状态
    if state == KazooState.LOST:
        print 'lost'
    elif state == KazooState.SUSPENDED:
        print 'suspended'
    else:
        print 'connected'


# .........................................................事务, 要么全部执行成功，要么全部失败
transaction = zk.transaction()
transaction.check('/china/hebei', version=3)
transaction.create('/china/shanxi', b"thi is shanxi.")
results = transaction.commit()
# .........................................................断开连接
zk.stop()
