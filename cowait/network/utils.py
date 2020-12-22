import socket
from .const import WS_PATH, QUERY_TOKEN


def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_local_url():
    local_ip = get_local_ip()
    return f'ws://{local_ip}/{WS_PATH}'


def get_remote_url(host, token):
    return f'ws://{host}/{WS_PATH}?{QUERY_TOKEN}={token}'
