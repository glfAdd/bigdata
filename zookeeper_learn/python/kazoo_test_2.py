#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
"""
有分布式锁和没分布式锁演示
"""
import os
import arrow
import redis
from multiprocessing import Pool
from kazoo.client import KazooClient

HOT_KEY = 'count'
r = redis.Redis(host='localhost', port=6379)


def seckilling():
    name = os.getpid()
    v = r.get(HOT_KEY)
    if int(v) > 0:
        print name, ' decr redis.'
        r.decr(HOT_KEY)
    else:
        print name, ' can not set redis.', v


def run_without_lock(name):
    while True:
        if arrow.now().second % 5 == 0:
            seckilling()
            return


def run_with_zk_lock(name):
    zk = KazooClient()
    zk.start()
    lock = zk.Lock("/lockpath", "my-identifier")
    while True:
        if arrow.now().second % 5 == 0:
            with lock:
                seckilling()
                return


if __name__ == '__main__':
    p = Pool(16)
    r.set(HOT_KEY, 1)
    for i in range(16):
        # 没有分布式锁
        # p.apply_async(run_without_lock, args=(i,))
        # 分布式锁
        p.apply_async(run_with_zk_lock, args=(i,))
    p.close()
    p.join()
