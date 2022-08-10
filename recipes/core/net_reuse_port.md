# TCP/UDP Reuse Port

Since Linux *3.9*. Improved in Linux *4.6*.

The socket option **`SO_REUSEPORT`** allows *`accept()`* **load distribution** in a multi-threaded server
to be improved by using a distinct listener socket for each thread.
This provides improved load distribution as compared to traditional techniques
such using a single `accept()`ing thread that distributes connections,
or having multiple threads that compete to `accept()` from the same socket.

```python
sock.setsocketopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
```

![socket SO_REUSEPORT](https://leven-cn.github.io/python-handbook/imgs/socket_SO_REUSEPORT.png)

In kernel, hash algorithms are used:

![socket SO_REUSEPORT using hash algorithms](https://leven-cn.github.io/python-handbook/imgs/socket_SO_REUSEPORT_hash.png)

See [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_REUSEPORT).

## Examples (Recipes)

- [TCP/UDP Reuse Port](https://leven-cn.github.io/python-cookbook/recipes/core/net_reuse_port)
- [TCP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_std)
- [TCP Server (IPv4) - Blocking Mode (阻塞模式)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_blocking)
- [TCP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_timeout)
- [TCP Server (IPv4) - Non-Blocking Mode (I/O Multiplex, I/O 多路复用)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_ipv4_io_multiplex)
- [TCP Server - Asynchronous I/O (异步 I/O) (High-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_high_api)
- [TCP Server - Asynchronous I/O (异步 I/O) (Low-Level APIs)](https://leven-cn.github.io/python-cookbook/recipes/core/tcp_server_asyncio_low_api)
- [UDP Server (IPv4) - Standard Framework](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_std)
- [UDP Server (IPv4) - Timeout Mode](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_ipv4_timeout)
- [UDP Server - Asynchronous I/O (异步 I/O)](https://leven-cn.github.io/python-cookbook/recipes/core/udp_server_asyncio)

## References

<!-- markdownlint-disable line-length -->

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Linux Programmer's Manual - socket(7)](https://manpages.debian.org/bullseye/manpages/socket.7.en.html)
- [Linux Programmer's Manual - socket(7) - `SO_REUSEPORT`](https://manpages.debian.org/bullseye/manpages/socket.7.en.html#SO_KEEPALIVE)

<!-- markdownlint-enable line-length -->
