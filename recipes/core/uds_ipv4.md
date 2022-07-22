# UNIX Domain Socket (IPv4)

UDS = UNIX Domain Socket

## Server

```python
import logging
import socket
from contextlib import suppress


sockfile = 'xxx.sock'

# Make sure the socket does not already exist.
with suppress(FileNotFoundError):
    os.remove(sockfile)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# bind
sock.bind(sockfile)
sock.listen()

try:
    while True:
        conn, client_address = sock.accept()
        with conn:
            while True:
                raw_data: bytes = conn.recv(1024)
                if raw_data:
                    data = raw_data.decode('utf-8')
                    logging.debug(f'receive data {data} from {client_address}')
                    conn.sendall(raw_data)
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


sockfile = 'xxx.sock'

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    try:
        client.connect(('localhost', 9999))
        client.sendall(b'data')
        client.recv(1024)
    except OSError as err:
        # error handling
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
