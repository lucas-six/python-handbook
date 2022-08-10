# TCP Keep-Alive

## `tcp_keepalive_time`

Since Linux *2.2*.

The number of seconds a connection needs to be idle before TCP begins sending out keep-alive probes.

(空闲时，启动探测间隔时间（秒）)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_time
7200
$ sysctl net.ipv4.tcp_keepalive_time
net.ipv4.tcp_keepalive_time = 7200

$ sudo sysctl -w net.ipv4.tcp_keepalive_time = 3600
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time).

Since Linux *2.4*.

```python
sock.setsocketopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 3600)

# macOS & Python 3.10+
if sys.platform == 'darwin' and sys.version >= (3, 10):
    sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, 3600)
```

See [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE),
and [Linux Programmer's Manual - tcp(7) - `TCP_KEEPIDLE`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE).

## `tcp_keepalive_probes`

Since Linux *2.2*.

The maximum number of TCP keep-alive probes to send before giving up and killing the connection
if no response is obtained from the other end.

(网络不可达时，重发探测次数)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_probes
9
$ sysctl net.ipv4.tcp_keepalive_probes
net.ipv4.tcp_keepalive_probes = 9

$ sudo sysctl -w net.ipv4.tcp_keepalive_probes = 9
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes).

Since Linux *2.4*.

```python
sock.setsocketopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 9)
```

See [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE),
and [Linux Programmer's Manual - tcp(7) - `TCP_KEEPCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT).

## `tcp_keepalive_intvl`

Since Linux *2.4*.

The number of seconds between TCP keep-alive probes.

(网络不可达时，重发探测间隔时间（秒）)

```bash
$ cat /proc/sys/net/ipv4/tcp_keepalive_intvl
75
$ sysctl net.ipv4.tcp_keepalive_intvl
net.ipv4.tcp_keepalive_intvl = 75

$ sudo sysctl -w net.ipv4.tcp_keepalive_intvl = 25
```

See [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl).

Since Linux *2.4*.

```python
sock.setsocketopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 25)
```

See [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE),
and [Linux Programmer's Manual - tcp(7) - `TCP_KEEPINTVL`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL).

## Examples (Recipes)

- [TCP Keep-Alive](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_keepalive)
- [TCP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_std)
- [TCP Server (IPv4) - Blocking Mode (阻塞模式)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_blocking)
- [TCP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_timeout)
- [TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O 多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_io_multiplex)
- [TCP Server - Asynchronous I/O (异步 I/O) (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_high_api)
- [TCP Server - Asynchronous I/O (异步 I/O) (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_low_api)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_KEEPALIVE`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPIDLE`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPIDLE)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_KEEPINTVL`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_KEEPINTVL)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_time`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_time)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_probes`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_probes)
- [Linux Programmer's Manual - tcp(7) - `tcp_keepalive_intvl`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_keepalive_intvl)
- [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793)

<!-- markdownlint-enable line-length -->
