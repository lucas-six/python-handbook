# IP Multicast

IPv4 range from `224.0.0.0` to `239.255.255.255` (D class).

## Usage

The **`IP_MULTICAST_TTL`** (for IPv4) and **`IPV6_MULTICAST_HOPS`** (for IPv6) socket options
allow the application to primarily limit the lifetime, *TTL* (Time to Live) or hops,
of the packet in the Internet
and prevent it from circulating indefinitely.

```python
# IPv4
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)  # default 1

# IPv6
sock.setsockopt(socket.IPPROTO_IP, socket.IPV6_MULTICAST_HOPS, 1)  # default 1
```

## References

- [Wikipedia - Multicast](https://en.wikipedia.org/wiki/Multicast)
- [Wikipedia - IP Multicast](https://en.wikipedia.org/wiki/IP_multicast)
- [RFC 1112 - Host Extensions for IP Multicasting](https://datatracker.ietf.org/doc/html/rfc1112)
- [RFC 2236 - Internet Group Management Protocol, Version 2](https://datatracker.ietf.org/doc/html/rfc2236)
- [RFC 3376 - Internet Group Management Protocol, Version 3](https://datatracker.ietf.org/doc/html/rfc3376)
- [RFC 4604 - Using Internet Group Management Protocol Version 3 (IGMPv3) and Multicast Listener Discovery Protocol Version 2 (MLDv2) for Source-Specific Multicast](https://datatracker.ietf.org/doc/html/rfc4604)
- [RFC 3810 - Multicast Listener Discovery Version 2 (MLDv2) for IPv6](https://datatracker.ietf.org/doc/html/rfc3810)
- [RFC 2710 - Multicast Listener Discovery (MLD) for IPv6](https://datatracker.ietf.org/doc/html/rfc2710)
- [RFC 3590 - Source Address Selection for the Multicast Listener Discovery (MLD) Protocol](https://datatracker.ietf.org/doc/html/rfc3590)
