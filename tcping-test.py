from tcping import Ping


ping = Ping('104.155.201.52', 80, 5)
ping.ping(10)
