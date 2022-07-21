# TCP (IPv4)

## Server

```python
import logging
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket.INADDR_LOOPBACK: 'localhost'
# socket.INADDR_ANY: '' or '0.0.0.0'
# socket.INADDR_BROADCAST
sock.bind(('localhost', 9999))
server_address = sock.getsockname()
sock.listen()

try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if data:
                    logging.debug(f'receive data from {client_address}')
                    conn.sendall(data)
                else:
                    logging.debug(f'no data from {client_address}')
                    break
            conn.shutdown(socket.SHUT_WR)
finally:
    sock.close()
```

## Client

```python
import socket

client = socket.create_connection(('localhost',9999))
client.sendall(b'data')
client.recv(1024)
client.close()
```

Or

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost',9999))
client.sendall(b'data')
client.recv(1024)
client.close()
```

## Reuse Address

The **`SO_REUSEADDR`** flag tells the kernel to reuse a local socket in **`TIME_WAIT`** state,
without waiting for its natural timeout to expire.

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

## `listen` Queue

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

```python
import os
from pathlib import Path
from typing import Final


accept_queue_size = 1024


if os.uname().sysname == 'Linux':
    max_syn_queue_size: Final[int] = int(
        Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
    )
    max_accept_queue_size: Final[int] = int(
        Path('/proc/sys/net/core/somaxconn').read_text().strip()
    )
    assert socket.SOMAXCONN == max_accept_queue_size

    accept_queue_size = min(max(backlog, 0), max_accept_queue_size)
    sock.listen(accept_queue_size)
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `listen`(2)](https://manpages.debian.org/bullseye/manpages-dev/listen.2.en.html)
