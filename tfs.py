#!/usr/bin/env python

import sys, commands

def usage():
    print "Usage: python tfs.py [status | start | stop]"

def status():
    cmds = [
        "ssh NS 'ps aux | grep -v grep | grep /app/tfs/bin/nameserver'",
        "ssh DS1 'ps aux | grep -v grep | grep /app/tfs/bin/dataserver'",
        "ssh DS2 'ps aux | grep -v grep | grep /app/tfs/bin/dataserver'",
        "ssh nginx 'ps aux | grep -v grep | grep /usr/local/nginx/sbin/nginx'"
    ]
    for cmd in cmds:
        res = commands.getoutput(cmd)
        print res
        if not res:
            return False
    return True

def start():
    cmds = [
        "ssh DS1 '/app/tfs/scripts/tfs start_ds 1-2'",
        "ssh DS2 '/app/tfs/scripts/tfs start_ds 1-2'",
        "ssh NS '/app/tfs/scripts/tfs start_ns'",
        "ssh nginx '/usr/local/nginx/sbin/nginx'"
    ]
    for cmd in cmds:
        res = commands.getoutput(cmd)
        print res

def stop():
    cmds = [
        "ssh nginx '/usr/local/nginx/sbin/nginx -s stop'"
        "ssh NS '/app/tfs/scripts/tfs stop_ns'",
        "ssh DS1 '/app/tfs/scripts/tfs stop_ds_all'",
        "ssh DS2 '/app/tfs/scripts/tfs stop_ds_all'",
    ]
    for cmd in cmds:
        res = commands.getoutput(cmd)
        print res

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
