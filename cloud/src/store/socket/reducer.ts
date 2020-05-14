import { SocketState, SocketActionTypes } from './types'
import { Reducer } from 'redux'

export const SOCKET_CONNECTED = 'socket_connected'
export const SOCKET_CONNECTING = 'socket_connecting'
export const SOCKET_ERROR = 'socket_error'
export const SOCKET_CLOSED = 'socket_closed'

const initialState: SocketState = {
    status: SOCKET_CONNECTING,
    error: undefined
}

const reducer: Reducer<SocketState> = (state = initialState, action) => {
    switch(action.type) {
    case SocketActionTypes.CONNECTING:
        return {
            ...state,
            status: SOCKET_CONNECTING,
        }
    case SocketActionTypes.CONNECTED:
        return {
            ...state,
            status: SOCKET_CONNECTED,
            error: undefined,
        }
    case SocketActionTypes.ERROR:
        return {
            ...state,
            status: SOCKET_ERROR,
            error: action.error,
        }
    default:
        return state
    }
}

export default reducer
