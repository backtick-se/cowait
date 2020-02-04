

export const SOCKET_CONNECTING = 'socket_connecting'
export const SOCKET_CONNECTED = 'socket_connected'
export const SOCKET_ERROR = 'socket_error'
export const SOCKET_CLOSED = 'socket_closed'

export function connecting() {
    return {
        type: SOCKET_CONNECTING,
    }
}

export function connected() {
    return {
        type: SOCKET_CONNECTED,
    }
}

export function error(error) {
    return {
        type: SOCKET_ERROR,
        error,
    }
}

export function closed() {
    return {
        type: SOCKET_CLOSED,
    }
}