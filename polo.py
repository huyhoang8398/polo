import argparse
import os
import socket
import subprocess
import re
import sys
import fcntl

def is_port_available(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.bind((ip, port))
        return True
    except OSError:
        return False

def warnf(format, *args):
    print("::", format % args, file=sys.stderr)

def close_on_exec(state):
    pid = os.getpid()
    out = subprocess.check_output(["ls", f"/proc/{pid}/fd/"]).decode("utf-8")
    pids = re.split("[ \t\n]", out)
    for pid_str in pids:
        if not pid_str:
            continue
        fd = int(pid_str)
        if fd > 2:
            flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            if state:
                flags |= fcntl.FD_CLOEXEC
            else:
                flags &= ~fcntl.FD_CLOEXEC
            fcntl.fcntl(fd, fcntl.F_SETFD, flags)

def main():
    parser = argparse.ArgumentParser(description="A Python version of solo")
    parser.add_argument("--address", default="127.0.0.1", help="Address to listen on or to check")
    parser.add_argument("--dir", default=".", help="Working directory")
    parser.add_argument("--port", type=int, default=0, help="Port to listen on or to check")
    parser.add_argument("--timeout", type=int, default=1, help="Timeout when checking. Default: 1 second.")
    parser.add_argument("--no-bind", action="store_true", help="Do not bind on address:port specified")
    parser.add_argument("command", nargs="+", help="The command to execute")

    args = parser.parse_args()

    if args.no_bind:
        if is_port_available(args.address, args.port, args.timeout):
            warnf("Port is available. App is not running")
        else:
            warnf("Port is not available. App is running?")
            sys.exit(0)
    else:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((args.address, args.port))
            warnf("Bind successfully on %s:%d", args.address, args.port)
        except OSError:
            warnf("Unable to bind on %s:%d. App is running?", args.address, args.port)
            sys.exit(1)

    os.chdir(args.dir)

    exec_path = args.command[0]

    if not args.no_bind:
        warnf("Making sure all fd >= 3 is not close-on-exec")
        close_on_exec(False)

    warnf("Now starting application '%s' from %s\n", exec_path, args.dir)

    try:
        os.execvp(exec_path, args.command)
    except Exception as e:
        warnf("Executing got error '%s'", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
