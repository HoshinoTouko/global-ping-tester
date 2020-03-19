import subprocess

from Core.TCPing import TCPing


class Ping:
    @classmethod
    def icmping(
            cls, ip_addr, label, trig_time,
            count=10, size=32, logger=print
    ):
        params = []
        if count:
            params.append('-n %s' % count)
        if size:
            params.append('-l %s ' % size)
        _command = 'ping.exe %s %s' % (str(ip_addr), ' '.join(params))
        # print('Execute', _command)
        res = subprocess.check_output(
            _command,
            # stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, shell=True
        )
        logger(ip_addr, label, trig_time, 'icmping', res)
        return res

    @classmethod
    def tcping(
            cls, ip_addr, label, trig_time,
            count=10, size=None, logger=print
    ):
        tcping = TCPing(ip_addr)
        res = tcping.ping(count)
        logger(ip_addr, label, trig_time, 'tcping', res)
        return res
