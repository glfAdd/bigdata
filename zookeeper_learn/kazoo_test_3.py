#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
"""
zookeeper 分布式锁
"""
import logging, arrow
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock

# 设置logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

zk_client = KazooClient(hosts='localhost:2181', timeout=5, logger=logger)
zk_client.start()
zk_lock = Lock(client=zk_client, path='/lock/lock_test_0001')

# 获取锁
a = zk_lock.acquire(blocking=True, timeout=None)
print arrow.now(), a
b = zk_lock.acquire(blocking=True, timeout=30)
print arrow.now(), b

zk_lock.release()
zk_client.stop()
