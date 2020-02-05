import * as actions from './actions'

const DefaultState = {
    status: actions.SOCKET_CONNECTING,
    error: false,
}

export function socket(state, action) {
    if (typeof(state) == 'undefined') {
        return DefaultState
    }

    switch(action.type) {
    case actions.SOCKET_CONNECTING:
        return {
            ...state,
            status: actions.SOCKET_CONNECTING,
        }

    case actions.SOCKET_CONNECTED:
        return {
            ...state,
            status: actions.SOCKET_CONNECTED,
            error: false,
        }

    case actions.SOCKET_ERROR:
        return {
            ...state,
            status: actions.SOCKET_CONNECTING,
            error: action.error,
        }
        
    default:
        return state
    }
}

export default socket