from collections import OrderedDict
from Core.Ping import Ping

import os
import multiprocessing
import subprocess
import time
import random


def first(s):
    """
    Return the first element from an ordered collection
    or an arbitrary element from an unordered collection.
    Raise StopIteration if the collection is empty.
    https://stackoverflow.com/questions/21062781/shortest-way-to-get-first-item-of-ordereddict-in-python-3/27666721
    """
    return next(iter(s))


class PingTester:
    def __init__(self):
        self.processes_pool = multiprocessing.Pool(processes=10)
        self.ipaddrs = {}
        self.scheduled = OrderedDict()

        self.started_at = 0
        self.end_at = 0

    def start(self, clear=False):
        if clear:
            # Clear history logs.
            old_logs = os.walk('./logs')
            for root, _, filenames in old_logs:
                for filename in filenames:
                    if filename.endswith('.log'):
                        full_path = os.path.join(root, filename)
                        print('Remove file:', full_path)
                        os.remove(full_path)

        # Do scheduled ping tasks
        while self.scheduled:
            now = int(time.time())
            while self.scheduled and first(self.scheduled) <= now:
                scheduled_time = first(self.scheduled)
                labels = self.scheduled[scheduled_time]
                for label in labels:
                    ip_addrs = self.ipaddrs.get(label)
                    if not ip_addrs:
                        break
                    ip_addr = random.choice(ip_addrs)
                    self.icmping(ip_addr, label, int(time.time()), logger=self.log)
                del self.scheduled[scheduled_time]
            time.sleep(0.9)

    def schedule(self, interval, period=600):
        started_at = int(time.time())

        step = 1 if interval > len(self.ipaddrs.keys()) else len(self.ipaddrs.keys()) / interval
        for _round in range(int(period / interval)):
            offset = 0.
            for ip_addr in self.ipaddrs.keys():
                estimate = int(started_at + _round * interval + offset)
                if estimate not in self.scheduled.keys():
                    self.scheduled[estimate] = []
                self.scheduled[estimate].append(ip_addr)
                offset += step

        self.started_at = started_at
        self.end_at = started_at + period

    def load_data(self, line: str):
        line = line.strip()
        if not line or line[0] == '#':
            return
        try:
            label, ipaddrs = line.split('-')
            label = label.strip()
            ipaddrs_list = ipaddrs.strip().split()
            if label not in self.ipaddrs:
                self.ipaddrs[label] = []
            self.ipaddrs[label] = list(set(self.ipaddrs[label] + ipaddrs_list))
        except:
            print('Invalid line:', line)

    def load_ipaddr(self, database=None):
        datafiles = []
        if database:
            datafiles = [database]
        else:
            iter_paths = os.walk('./ipaddr_dataset')
            for iter_path in iter_paths:
                root, _, file_list = iter_path
                for file in file_list:
                    if file.endswith('.ipaddr'):
                        datafiles.append(os.path.join(root, file))
        for datafile in datafiles:
            fi = open(datafile)
            for line in fi.readlines():
                self.load_data(line)

    def icmping(self, ip_addr, label, trig_time, **kwargs):
        if 'TCPingOnly' not in label:
            print('ICMP Ping start:', label, ip_addr, trig_time)
            self.processes_pool.apply_async(
                Ping.icmping, (ip_addr, label, trig_time), kwargs,
            )
        print('TCP Ping start:', label, ip_addr, trig_time)
        self.processes_pool.apply_async(
            Ping.tcping, (ip_addr, label, trig_time), kwargs,
        )

    # Deprecated
    # def _ping(self, ip_addr, label, trig_time, params):
    #     # sys.stdout = open(str(os.getpid()) + ".out", "a", buffering=0)
    #
    #     _command = 'ping.exe %s %s' % (str(ip_addr), ' '.join(params))
    #     # print('Execute', _command)
    #     res = subprocess.check_output(
    #         _command,
    #         # stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #         universal_newlines=True, shell=True
    #     )
    #     self.log(ip_addr, label, trig_time, res)
    #     return res

    def log(self, ip_addr, label, trig_time, ping_type, result):
        with open('./logs/[%s] %s.log' % (ping_type.upper(), label), 'a') as fi:
            fi.write('%s: %s\n%s\n----------\n' % (
                trig_time, ip_addr, result
            ))

    def wait_for_end(self):
        self.processes_pool.close()
        self.processes_pool.join()

    # We should init our customize get function because the pool objects cannot be pickled
    def __getstate__(self):
        self_dict = self.__dict__.copy()
        # print(self.__dict__)
        del self_dict['processes_pool']
        return self_dict

    def __setstate__(self, state):
        # print(state)
        self.__dict__.update(state)


def main():
    tester = PingTester()
    tester.load_ipaddr()
    tester.schedule(30, 300)
    tester.start(clear=True)

    tester.wait_for_end()


if __name__ == "__main__":
    main()
