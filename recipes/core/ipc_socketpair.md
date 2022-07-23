# IPC - Socket Pair

IPC between parent and child processes.

## Usage

```python
import socket


parent, child = socket.socketpair()  # AF_UNIX by default
assert isinstance(parent, socket.SocketType)
assert isinstance(child, socket.SocketType)

pid = os.fork()
if pid:
    # parent process
    child.close()
    parent.sendall(b'data')
    data: bytes = parent.recv(1024)
    parent.close()
else:
    # child process
    parent.close()
    data: bytes = child.recv(1024)
    child.sendall(data)
    child.close()
```

## References

- [Python - `socket.socketpair()`](https://docs.python.org/3/library/socket.html#socket.socketpair)
