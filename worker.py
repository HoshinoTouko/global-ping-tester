#!/usr/bin/python3

from ping import PingTester

import sys


def main(argv):
    interval = argv[1]
    period = argv[2]

    tester = PingTester()
    tester.load_ipaddr()
    tester.schedule(int(interval), int(period))
    tester.start(clear=True)

    tester.wait_for_end()


if __name__ == '__main__':
    main(sys.argv)
