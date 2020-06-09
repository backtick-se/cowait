import { SOCKET_CONNECTING, SOCKET_CONNECTED, SOCKET_ERROR, SOCKET_CLOSED } from './reducer';

export type SOCKET_CONNECTING = typeof SOCKET_CONNECTING
export type SOCKET_CONNECTED = typeof SOCKET_CONNECTED
export type SOCKET_ERROR = typeof SOCKET_ERROR
export type SOCKET_CLOSED = typeof SOCKET_CLOSED

export type SocketStatus = SOCKET_CONNECTING | SOCKET_CONNECTED | SOCKET_ERROR | SOCKET_CLOSED

export enum SocketActionTypes {
  CONNECTING = '@@socket/CONNECTING',
  CONNECTED = '@@socket/CONNECTED',
  ERROR = '@@socket/ERROR',
  CLOSED = '@@socket/CLOSED'
}

export type SocketState = {
  status: SocketStatus,
  error?: WebSocketCloseEvent
}

