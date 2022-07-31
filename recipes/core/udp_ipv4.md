# UDP (IPv4)

UDP = User Datagram Protocol

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

## Timeout

- **blocking mode** (default): `socket.settimeout(None)` or `socket.setblocking(True)`
- **timeout mode**: `socket.settimeout(3.5)`
- **non-blocking mode**: `socket.settimeout(0.0)` or `socket.setblocking(False)`

affect `connect()`, `accept()`, `send()`/`sendall()`/`sendto()`, `recv()`/`recvfrom()`.

## Examples (Recipes)

- [UDP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_std)
- [UDP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_timeout)
- [UDP Client (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_client_ipv4_timeout)

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - udp(7)](https://manpages.debian.org/bullseye/manpages/udp.7.en.html)
- [Linux Programmer's Manual - `socket`(2)](https://manpages.debian.org/bullseye/manpages-dev/socket.2.en.html)
- [Linux Programmer's Manual - `bind`(2)](https://manpages.debian.org/bullseye/manpages-dev/bind.2.en.html)
- [Linux Programmer's Manual - `getsockname`(2)](https://manpages.debian.org/bullseye/manpages-dev/getsockname.2.en.html)
- [Linux Programmer's Manual - `recvfrom`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `sendto`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
