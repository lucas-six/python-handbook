# TCP (IPv4)

TCP = Transmission Control Protocol

See [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793).

## `listen()` Queue

Because of the 3-way handshake used by TCP,
an incoming connection goes through an intermediate state **`SYN RECEIVED`**
before it reaches the **`ESTABLISHED`** state
and can be returned by the **`accept()`** syscall to the application.
This means that a TCP/IP stack has two options
to implement the backlog queue for a socket in *`LISTEN`* state:

1. The implementation uses a single queue,
the size of which is determined by the *`backlog`* argument of the *`listen()`* syscall.
When a `SYN` packet is received, it sends back a `SYN`/`ACK` packet and adds the connection to the queue.
When the corresponding `ACK` is received, the connection changes its state to `ESTABLISHED`
and becomes eligible for handover to the application.
This means that the queue can contain connections in two different state: `SYN RECEIVED` and `ESTABLISHED`.
Only connections in the latter state can be returned to the application by the *`accept()`* syscall.
2. The implementation uses two queues, a `SYN` queue(or incomplete connection queue)
and an accept queue (or complete connection queue).
Connections in state `SYN RECEIVED` are added to the `SYN` queue
and later moved to the accept queue when their state changes to `ESTABLISHED`,
i.e. when the `ACK` packet in the 3-way handshake is received.
As the name implies,
the *`accept()`* call is then implemented simply to consume connections from the accept queue.
In this case, the `backlog` argument of the *`listen()`* syscall determines the size of the accept queue.

Historically, *BSD* derived TCP implementations use the first approach.
That choice implies that when the maximum `backlog` is reached,
the system will no longer send back `SYN`/`ACK` packets in response to `SYN` packets.
Usually the TCP implementation will simply drop the `SYN` packet
(instead of responding with a `RST` packet) so that the client will retry.

On *Linux*, things are different, as mentioned in the man page of the *`listen()`* syscall:
The behavior of the `backlog` argument on TCP sockets changed with Linux *2.2*.
Now it specifies the queue length for completely established sockets waiting to be accepted,
instead of the number of incomplete connection requests.

This means that current Linux versions use the second option with two distinct queues:
a `SYN` queue with a size specified by a system wide setting
and an accept queue with a size specified by the application.

The maximum length of the `SYN` queue for incomplete sockets can be set using:

```bash
/proc/sys/net/ipv4/tcp_max_syn_backlog
```

or

```bash
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=<N>
```

or make the change permanently in **`/etc/sysctl.conf`**.

While the maximum length of the aceept queue for completed sockets can be set using:

```bash
/proc/sys/net/core/somaxconn
```

or

```bash
sudo sysctl -w net.core.somaxconn=<N>
```

or make the change permanently in **`/etc/sysctl.conf`**.

## Timeout

### Application Level

- **blocking mode** (default): `socket.settimeout(None)` or `socket.setblocking(True)`
- **timeout mode**: `socket.settimeout(3.5)`
- **non-blocking mode**: `socket.settimeout(0.0)` or `socket.setblocking(False)`

affect `connect()`, `accept()`, `send()`/`sendall()`/`sendto()`, `recv()`/`recvfrom()`.

### Client Connect Timeout (Linux)

Since Linux *2.2*.

```bash
cat /proc/sys/net/ipv4/tcp_syn_retries
```

or

```bash
sysctl -w net.ipv4.tcp_syn_retries = 2
```

The maximum number of times initial `SYN`s for an active TCP connection attempt will be retransmitted.
This value should not be higher than *`255`*. The default value is *`6`*,
which corresponds to retrying for up to approximately *127 seconds*.

```c
// linux kernel 2.6.32
icsk->icsk_rto = min(icsk->icsk_rto << 1, TCP_RTO_MAX)
```

means

```python
def linux_connect_timeout(tcp_syn_retries: int) -> int:
    r = tcp_syn_retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (tcp_syn_retries - r)
    return timeout
```

Before Linux *3.7*, the default value was *`5`*,
which (in conjunction with calculation based on other kernel parameters)
corresponded to approximately *180 seconds*.

See [Linux - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)

```python
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_SYNCNT, 2)
```

See [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT).

### Server Connect Timeout (Linux)

Since Linux *2.2*.

```bash
cat /proc/sys/net/ipv4/tcp_synack_retries
```

or

```bash
sysctl -w net.ipv4.tcp_synack_retries = 2
```

The maximum number of times a `SYN`/`ACK` segment for a passive TCP connection will be retransmitted.
This number should not be higher than *`255`*.
See [Linux - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)

```c
// linux kernel 2.6.32
icsk->icsk_rto = min(icsk->icsk_rto << 1, TCP_RTO_MAX)
```

means

```python
def linux_connect_timeout(tcp_synack_retries: int) -> int:
    r = tcp_synack_retries
    timeout = 1
    while r:
        r -= 1
        timeout += 2 ** (tcp_synack_retries - r)
    return timeout
```

### Recv/Send Timeout (Linux)

The **`SO_RCVTIMEO`** and **`SO_SNDTIMEO`** socket options
specify the receiving or sending timeouts.

Retransmission: *RTO* (Retransmission Time-Out), *RTT* (Round Trip Time),

[RFC 6298](https://datatracker.ietf.org/doc/html/rfc6298.html) suggests:

```plaintext
new_RTTs = (1 - α) × (old_RTTs) + α × (new_RTT_sample), 0 <= α < 1 (0.125 recommended)
RTO = RTTs + 4 × RTTd
new_RTTd = (1 - β) × (old_RTTd) + β × |RTTs - new_RTT_sample|, 0 <= β < 1 (0.25 recommended)
```

*Karn's algorithm*.

Set TCP retransmission times, since Linux *2.2*:

```bash
$ sysctl net.ipv4.tcp_retries1
3
$ sysctl net.ipv4.tcp_retries2
15

sysctl -w net.ipv4.tcp_retries1 = 3
sysctl -w net.ipv4.tcp_retries2 = 5
```

## Receive/Send Buffer

### OS Level (Linux)

```bash
# recv buffer
# - default: 208KB
# - max: 208KB
$ cat /proc/sys/net/core/rmem_max
212992
$ sysctl net.core.rmem_max
net.core.rmem_max = 212992
$ cat /proc/sys/net/core/rmem_default
212992
$ sysctl net.core.rmem_default
net.core.rmem_default = 212992

# send buffer
# - default: 208KB
# - max: 208KB
$ cat /proc/sys/net/core/wmem_max
212992
$ sysctl net.core.wmem_max
net.core.wmem_max = 212992
$ cat /proc/sys/net/core/wmem_default
212992
$ sysctl net.core.wmem_default
net.core.wmem_default = 212992

$ cat /proc/sys/net/ipv4/tcp_rmem
4096    131072  6291456
$ sysctl net.ipv4.tcp_rmem
net.ipv4.tcp_rmem = 4096        131072  6291456
$ cat /proc/sys/net/ipv4/tcp_wmem
4096    16384   4194304
$ sysctl net.ipv4.tcp_wmem
net.ipv4.tcp_rmem = 4096        16384   4194304
$ cat /proc/sys/net/ipv4/tcp_window_scaling
1
$ sysctl -w net.ipv4.tcp_window_scaling = 1
```

### Application Level

```python
# recv buffer
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, N)
recv_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

# send buffer
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, N)
send_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
```

## Nagle Algorithm (`TCP_NODELAY`)

Nagle's algorithm works by combining a number of small outgoing messages and sending them all at once.
It was designed to solve "small-packet problem".

Disable it:

```python
sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

See [RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1) (Obsoleted)](https://www.rfc-editor.org/rfc/rfc896)
and [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY).

## Delayed ACK (延迟确认) (`TCP_QUICKACK`)

Since Linux *2.4.4*.

The socket option **`SO_REUSEPORT`** allows *`accept()`* **load distribution** in a multi-threaded server
to be improved by using a distinct listener socket for each thread.
This provides improved load distribution as compared to traditional techniques
such using a single `accept()`ing thread that distributes connections,
or having multiple threads that compete to `accept()` from the same socket.

In quickack mode, *`ACK`*s are sent immediately,
rather than *delayed* if needed in accordance to normal TCP operation.

The **`TCP_QUICKACK`** flag is not permanent, it only enables a switch to or from quickack mode.
Subsequent operation of the TCP protocol will once again enter/leave quickack mode
depending on internal protocol processing and factors
such as delayed ack timeouts occurring and data transfer.
This option should not be used in code intended to be portable.

```python
sock.setsocketopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
```

See [RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7) (Obsoleted)](https://www.rfc-editor.org/rfc/rfc813)
and [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK).

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
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `selectors` module](https://docs.python.org/3/library/selectors.html)
- [Python - `select` module](https://docs.python.org/3/library/select.html)
- [Python - `asyncio` module](https://docs.python.org/3/library/asyncio.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [PEP 3156 – Asynchronous IO Support Rebooted: the "asyncio" Module](https://peps.python.org/pep-3156/)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
- [Linux Programmer's Manual - `select`(2)](https://manpages.debian.org/bullseye/manpages-dev/select.2.en.html)
- [Linux Programmer's Manual - `poll`(2)](https://manpages.debian.org/bullseye/manpages-dev/poll.2.en.html)
- [Linux Programmer's Manual - `epoll`(7)](https://manpages.debian.org/bullseye/manpages-dev/epoll.7.en.html)
- [Linux Programmer's Manual - `accept`(2)](https://manpages.debian.org/bullseye/manpages-dev/accept.2.en.html)
- [Linux Programmer's Manual - `connect`(2)](https://manpages.debian.org/bullseye/manpages-dev/connect.2.en.html)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEADDR`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEADDR)
- [Linux Programmer's Manual - socket(7) - `SO_RCVBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_RCVBUF)
- [Linux Programmer's Manual - socket(7) - `SO_SNDBUF`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_SNDBUF)
- [Linux Programmer's Manual - socket(7) - `rmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_default)
- [Linux Programmer's Manual - socket(7) - `rmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#rmem_max)
- [Linux Programmer's Manual - socket(7) - `wmem_default`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_default)
- [Linux Programmer's Manual - socket(7) - `wmem_max`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#wmem_max)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `TCP_SYNCNT`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_SYNCNT)
- [Linux Programmer's Manual - tcp(7) - `TCP_NODELAY`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_NODELAY)
- [Linux Programmer's Manual - tcp(7) - `TCP_QUICKACK`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#TCP_QUICKACK)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - tcp(7) - `tcp_rmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_wmem`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_wmem)
- [Linux Programmer's Manual - tcp(7) - `tcp_window_scaling`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_window_scaling)
- [Linux Programmer's Manual - tcp(7) - `tcp_slow_start_after_idle`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_slow_start_after_idle)
- [Linux Programmer's Manual - tcp(7) - `tcp_rfc1337`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_rfc1337)
- [Linux Programmer's Manual - tcp(7) - `tcp_sack`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_sack)
- [RFC 793 - TRANSMISSION CONTROL PROTOCOL (1981.9)](https://www.rfc-editor.org/rfc/rfc793)
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 896 - Congestion Control in IP/TCP Internetworks (1984.1)](https://www.rfc-editor.org/rfc/rfc896) (Obsoleted by [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681))
- [RFC 813 - WINDOW AND ACKNOWLEDGEMENT STRATEGY IN TCP (1982.7) (Obsoleted)](https://www.rfc-editor.org/rfc/rfc813)
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
- [Wikipedia - Nagle's Algorithm](https://en.wikipedia.org/wiki/Nagle%27s_algorithm)
- [Wikipedia - TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_avoidance_algorithm)

<!-- markdownlint-enable line-length -->
