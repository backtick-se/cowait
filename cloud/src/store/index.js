import { 
    createStore as createReduxStore, 
    applyMiddleware, 
    combineReducers, 
} from 'redux'
import { createLogger } from 'redux-logger'
import tasks from './tasks'
import socket from './socket'


export function createStore({ logging }) {
    let middleware = [ ]
    if (logging) {
        middleware.push(createLogger())
    }

    return createReduxStore(
        combineReducers({
            tasks: tasks.reducer,
            socket: socket.reducer,
        }),
        applyMiddleware(
            ...middleware
        )
    )
}

export default createStore  