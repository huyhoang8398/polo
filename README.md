# NAME

`polo` -- Prevents a program from running more than one copy at a time

The basic ideas come from the original `Perl` application [solo](https://github.com/timkay/solo)

`polo` prevents a program from running more than one copy at a time; it is useful with `cron` to make sure that a job doesn't run before a previous one has finished.

# Example usage

```
usage: polo.py [-h] [--address ADDRESS] [--dir DIR] [--port PORT] [--timeout TIMEOUT] [--no-bind]
               command [command ...]

A Python version of solo

positional arguments:
  command            The command to execute

options:
  -h, --help         show this help message and exit
  --address ADDRESS  Address to listen on or to check
  --dir DIR          Working directory
  --port PORT        Port to listen on or to check
  --timeout TIMEOUT  Timeout when checking. Default: 1 second.
  --no-bind          Do not bind on address:port specified
```

Below the crontab settings to create some ssh tunnels. If any tunnel is broken due to network issue, cron will try to restart them in within 1 minute. If the tunnel is still work, cron will simply exit.

```bash
$ crontab -l

*/1 * * * * python solo.py --port 6432 --address 127.0.0.1 --no-bind -- /usr/bin/ssh zproxydev -fN
*/1 * * * * python solo.py --port 6442 --address 127.0.0.1 --no-bind -- /usr/bin/ssh zproxystaging -fN
*/1 * * * * python solo.py --port 6452 --address 127.0.0.1 --no-bind -- /usr/bin/ssh zproxyproduction -fN
```





