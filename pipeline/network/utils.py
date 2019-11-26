import socket


PORT = 1338


def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def get_local_connstr():
    local_ip = get_local_ip()
    return f'ws://{local_ip}:{PORT}'