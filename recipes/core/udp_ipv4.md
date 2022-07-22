# UDP (IPv4)

UDP = User Datagram Protocol

## Server

```python
import logging
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# socket.INADDR_LOOPBACK: 'localhost'
# socket.INADDR_ANY: '' or '0.0.0.0'
# socket.INADDR_BROADCAST
# Port 0 means to select an arbitrary unused port
sock.bind(('localhost', 0))
server_address = sock.getsockname()

try:
    while True:
        raw_data, client_address = sock.recvfrom(1024)
        if raw_data:
            data = raw_data.decode('utf-8')
            logging.debug(f'receive data {data} from {client_address}')
            sock.sendto(raw_data, client_address)
        else:
            logging.debug(f'no data from {client_address}')
            break
finally:
    sock.close()
```

## Client

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'data', ('localhost', 9999))
data, server_address = client.recvfrom(1024)
client.close()
```

## Reuse Address

The **`SO_REUSEADDR`** flag tells the kernel to reuse a local socket in **`TIME_WAIT`** state,
without waiting for its natural timeout to expire.

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
- [Linux Programmer's Manual - `recv`(2)](https://manpages.debian.org/bullseye/manpages-dev/recv.2.en.html)
- [Linux Programmer's Manual - `send`(2)](https://manpages.debian.org/bullseye/manpages-dev/send.2.en.html)
