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

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
