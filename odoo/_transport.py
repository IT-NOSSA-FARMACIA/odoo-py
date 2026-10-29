from __future__ import annotations
import xmlrpc.client

# Seconds a single network operation (connect, TLS handshake, read) may block.
# Without it an unresponsive Odoo hangs the caller until something outside
# kills it. Generous on purpose: legitimate heavy calls must not trip it.
DEFAULT_TIMEOUT = 300.0


class _TimeoutTransport(xmlrpc.client.Transport):
    def __init__(self, timeout: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._timeout = timeout

    def make_connection(self, host):
        connection = super().make_connection(host)
        connection.timeout = self._timeout
        return connection


class _TimeoutSafeTransport(xmlrpc.client.SafeTransport):
    def __init__(self, timeout: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._timeout = timeout

    def make_connection(self, host):
        connection = super().make_connection(host)
        connection.timeout = self._timeout
        return connection


def server_proxy(url: str, timeout: float) -> xmlrpc.client.ServerProxy:
    if url.lower().startswith("https"):
        transport = _TimeoutSafeTransport(timeout)
    else:
        transport = _TimeoutTransport(timeout)
    return xmlrpc.client.ServerProxy(url, transport=transport)
