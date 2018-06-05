#!/usr/bin/env python

import sys, commands

def usage():
    print "Usage: python tfs.py [status | start | stop]"

def execute(newcmds):
    for host, cmd in newcmds:
        print "[root@{} ~]# {}".format(host, cmd)
        res = commands.getoutput("ssh {} '{}'".format(host, cmd))
        print res

def status():
    newcmds = [
        # ["host", "cmd"],
        ["ns-master", "ps aux | grep -v grep | grep /app/tfs/bin/nameserver"],
        ["ds1", "ps aux | grep -v grep | grep /app/tfs/bin/dataserver"],
        ["ds2", "ps aux | grep -v grep | grep /app/tfs/bin/dataserver"],
        ["nginx", "ps aux | grep -v grep | grep /usr/local/nginx/sbin/nginx"],
    ]
    execute(newcmds)

def start():
    newcmds = [
        # ["host", "cmd"],
        ["ds1", "/app/tfs/scripts/tfs start_ds 1-2"],
        ["ds2", "/app/tfs/scripts/tfs start_ds 1-2"],
        ["ns-master", "/app/tfs/scripts/tfs start_ns"],
        ["nginx", "/usr/local/nginx/sbin/nginx"],
    ]
    execute(newcmds)

def stop():
    newcmds = [
        # ["host", "cmd"],
        ["nginx", "/usr/local/nginx/sbin/nginx -s stop"],
        ["ns-master", "/app/tfs/scripts/tfs stop_ns"],
        ["ds1", "/app/tfs/scripts/tfs stop_ds_all"],
        ["ds2", "/app/tfs/scripts/tfs stop_ds_all"],
    ]
    execute(newcmds)

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "status":
        status()
    elif len(sys.argv) == 2 and sys.argv[1] == "start":
        start()
    elif len(sys.argv) == 2 and sys.argv[1] == "stop":
        stop()
    else:
        usage()
        sys.exit()

if __name__ == '__main__':
    main()
