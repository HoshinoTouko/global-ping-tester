#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Code from https://github.com/zhengxiaowai/tcping/blob/master/tcping.py
"""
from six.moves import zip_longest
from timeit import default_timer as timer

import socket
import time


def avg(x):
    return sum(x) / float(len(x))


class Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Timer(object):
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip_longest(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start


class TCPing(object):
    def __init__(self, host, port=80, timeout=1):
        self.timer = Timer()

        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._timeout = timeout

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def _success_rate(self):
        count = self._successed + self._failed
        try:
            rate = (float(self._successed) / count) * 100
            rate = '{0:.2f}'.format(rate)
        except ZeroDivisionError:
            rate = '0.00'
        return rate

    @property
    def status(self):
        return self._successed == 0

    def ping(self, count=10):
        result = []
        for times in range(1, count + 1):
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                time.sleep(1)
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown),
                    ((self._host, self._port), None))
                s_runtime = 1000 * (cost_time)

                # result.append("Connected to %s[:%s]: seq=%d time=%.2f ms" % (
                #     self._host, self._port, times, s_runtime))
                result.append('%s %.4f' % (times, s_runtime))

                self._conn_times.append(s_runtime)
            except socket.timeout:
                # result.append("Connected to %s[:%s]: seq=%d timeout!" % (
                #     self._host, self._port, times))
                result.append('%s timeout' % times)
                self._failed += 1

            except KeyboardInterrupt:
                raise KeyboardInterrupt()

            else:
                self._successed += 1

            finally:
                s.close()
        return '\n'.join(result)


if __name__ == '__main__':
    pass
