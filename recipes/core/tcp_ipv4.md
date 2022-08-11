# TCP (IPv4)

TCP = Transmission Control Protocol

See [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793).

## Slow Start (慢启动)

Since Linux *2.6.18*.

**Slow start** is part of the *congestion control strategy* used by TCP
in conjunction with other algorithms to avoid sending more data than the network is capable of forwarding,
that is, to avoid causing network congestion.

Disable it:

```bash
sysctl -w net.ipv4.tcp_slow_start_after_idle=0
```

See [RFC 2001 - TCP Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Algorithms (1997.1)](https://www.rfc-editor.org/rfc/rfc2001)
(Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681)),
[RFC 2861 - TCP Congestion Window Validation (2000.6)](https://datatracker.ietf.org/doc/html/rfc2861.html)
(Obsoleted by [RFC 7661](https://datatracker.ietf.org/doc/html/rfc7661.html)),
and [Linux Programmer's Manual - tcp(7) - `tcp_slow_start_after_idle`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_slow_start_after_idle)

## TIME-WAIT Assassination Hazards (TIME-WAIT 暗杀)

```bash
$ cat /proc/sys/net/ipv4/tcp_rfc1337
0
$ sysctl net.ipv4.tcp_rfc1337
net.ipv4.tcp_rfc1337 = 0

$ sudo sysctl -w net.ipv4.tcp_rfc1337 = 1
```

See [Linux Programmer's Manual - tcp(7) - `tcp_rfc1337`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rfc1337)
and [RFC 1337 - TIME-WAIT Assassination Hazards in TCP (1992.5)](https://www.rfc-editor.org/rfc/rfc1337).

## Selective ACK (SACK)

Since Linux *2.2*.

```bash
sysctl -w net.ipv4.tcp_sack = 1
```

See [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html).

## Examples (Recipes)

- [TCP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_std)
- [TCP Server (IPv4) - Blocking Mode (阻塞模式)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_blocking)
- [TCP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_timeout)
- [TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O 多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_io_multiplex)
- [TCP Server - Asynchronous I/O (异步 I/O) (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_high_api)
- [TCP Server - Asynchronous I/O (异步 I/O) (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_low_api)
- [TCP Client (IPv4) - Basic](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_basic)
- [TCP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_timeout)
- [TCP Client (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O 多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_ipv4_io_multiplex)
- [TCP Client - Asynchronous I/O (异步 I/O) (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_asyncio_high_api)
- [TCP Client - Asynchronous I/O (异步 I/O) (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_client_asyncio_low_api)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_slow_start_after_idle`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_slow_start_after_idle)
- [Linux Programmer's Manual - tcp(7) - `tcp_rfc1337`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rfc1337)
- [Linux Programmer's Manual - tcp(7) - `tcp_sack`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_sack)
- [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793)
- [RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1)](https://www.rfc-editor.org/rfc/rfc896) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 7805 - Moving Outdated TCP Extensions and TCP-Related Documents to Historic or Informational Status (2016.4)](https://www.rfc-editor.org/rfc/rfc7805)
- [RFC 2001 - TCP Slow Start, Congestion Avoidance, Fast Retransmit, and Fast Recovery Algorithms (1997.1)](https://www.rfc-editor.org/rfc/rfc2001) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 2414 - Increasing TCP's Initial Window (1998.9)](https://www.rfc-editor.org/rfc/rfc2414) (Obsoleted by [RFC 3390](https://www.rfc-editor.org/rfc/rfc3390))
- [RFC 2581 - TCP Congestion Control (1999.4)](https://www.rfc-editor.org/rfc/rfc2581) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 3390 - Increasing TCP's Initial Window (2002.8)](https://www.rfc-editor.org/rfc/rfc3390)
- [RFC 5681 - TCP Congestion Control (2009.9)](https://www.rfc-editor.org/rfc/rfc5681)
- [RFC 1323 - TCP Extensions for High Performance (1992.5)](https://www.rfc-editor.org/rfc/rfc1323) (Obsoleted by [RFC 7323]((https://www.rfc-editor.org/rfc/rfc7323)))
- [RFC 7323 - TCP Extensions for High Performance (2014.9)](https://www.rfc-editor.org/rfc/rfc7323)
- [RFC 2861 - TCP Congestion Window Validation (2000.6)](https://datatracker.ietf.org/doc/html/rfc2861.html) (Obsoleted by [RFC 7661](https://datatracker.ietf.org/doc/html/rfc7661.html))
- [RFC 7661 - Updating TCP to Support Rate-Limited Traffic (2015.10)](https://datatracker.ietf.org/doc/html/rfc7661.html)
- [RFC 1337 - TIME-WAIT Assassination Hazards in TCP (1992.5)](https://www.rfc-editor.org/rfc/rfc1337)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
- [Wikipedia - TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_avoidance_algorithm)

<!-- markdownlint-enable line-length -->
