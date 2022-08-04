# TCP (IPv4)

TCP = Transmission Control Protocol

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

```bash
cat /proc/sys/net/ipv4/tcp_syn_retries
```

The maximum number of times initial `SYN`s for an active TCP connection attempt will be retransmitted.
This value should not be higher than *`255`*. The default value is *`6`*,
which corresponds to retrying for up to approximately *127 seconds*.
See [Linux - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)

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

### Server Connect Timeout (Linux)

```bash
cat /proc/sys/net/ipv4/tcp_synack_retries
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
```

Enable TCP **SACK** (**Selective ACKonwledgement**), since Linux *2.2*
see [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html):

```bash
sysctl -w net.ipv4.tcp_sack = 1
```

## Recv/Send Buffer

### OS Level (Linux)

```bash
# recv buffer
# - min: 4KB
# - default: 128KB
# - max: 6MB
$ cat /proc/sys/net/ipv4/tcp_rmem
4096 131072 6291456
$ sysctl net.ipv4.tcp_rmem
net.ipv4.tcp_rmem = 4096 131072 6291456

# send buffer
# - min: 4KB
# - default: 16KB
# - max: 4MB
$ cat /proc/sys/net/ipv4/tcp_wmem
4096 16384 4194304
$ sysctl net.ipv4.tcp_rmem
net.ipv4.tcp_rmem = 4096 16384 4194304
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

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [Python - `threading` module](https://docs.python.org/3/library/threading.html)
- [Python - `selectors` module](https://docs.python.org/3/library/selectors.html)
- [Python - `select` module](https://docs.python.org/3/library/select.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - tcp(7)](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html)
- [Linux Programmer's Manual - tcp(7) - `tcp_syn_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_syn_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_synack_retries`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_synack_retries)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries1`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries1)
- [Linux Programmer's Manual - tcp(7) - `tcp_retries2`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_retries2)
- [Linux Programmer's Manual - tcp(7) - `tcp_sack`](https://manpages.debian.org/bullseye/manpages/tcp.7.en.html#tcp_sack)
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
- [RFC 6298 - Computing TCP's Retransmission Timer](https://datatracker.ietf.org/doc/html/rfc6298.html)
- [RFC 2018 - TCP Selective Acknowledgment Options](https://datatracker.ietf.org/doc/html/rfc2018.html)
