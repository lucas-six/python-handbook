# `socketserver` - Standard Networks Server Framework

## Class Diagram

```mermaid
classDiagram
    BaseServer <|-- TCPServer
    BaseServer <|-- UDPServer
    TCPServer <|-- UnixStreamServer
    UDPServer <|-- UnixDatagramServer
    TCPServer <|-- ForkingTCPServer
    ForkingMixIn <|-- ForkingTCPServer
    UDPServer <|-- ForkingUDPServer
    ForkingMixIn <|-- ForkingUDPServer
    TCPServer <|-- ThreadingTCPServer
    ThreadingMixIn <|-- ThreadingTCPServer
    UDPServer <|-- ThreadingUDPServer
    ThreadingMixIn <|-- ThreadingUDPServer
    class BaseServer {
      +int address_family
      +tuple server_address
      +socket.socket socket
      +bool allow_reuse_address
      +int request_queue_size
      +int socket_type
      +float timeout
      +server_close() None
      +fileno() int
      +serve_forever() None
      +shutdown() None
      -handle_request() None
      -service_actions() None
      get_request()* Any
      verify_request()* bool
      process_request()* None
      finish_request()* None
      handle_timeout()* None
      handle_error()* None
      server_bind()* None
      server_activate()* None
    }
    class TCPServer {
      +int address_family
      +int socket_type
    }
    class UDPServer {
      +int address_family
      +int socket_type
    }
    class UnixStreamServer {
      +int address_family
    }
    class UnixDatagramServer {
      +int address_family
    }
```

## UDP Server

```python
import socketserver


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        print(f'{self.client_address[0]} wrote: {self.data}')
        sock.sendto(data.upper(), self.client_address)


if __name__ == "__main__":
    with socketserver.UDPServer(('localhost', 9999), MyUDPHandler) as server:
        server.serve_forever()
```

## References

- [Python - `socket` module](https://docs.python.org/3/library/socket.html)
- [Python - `socketserver` module](https://docs.python.org/3/library/socketserver.html)
- [PEP 3151 – Reworking the OS and IO exception hierarchy](https://peps.python.org/pep-3151/)
