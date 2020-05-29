import { 
    createStore as createReduxStore, 
    applyMiddleware,
    combineReducers
} from 'redux'
import { createLogger } from 'redux-logger'
import tasks from './tasks'
import socket from './socket'
import theme from './theme'
import { TaskState } from './tasks/types'
import { SocketState } from './socket/types'
import { ThemeState } from './theme/types'

type StoreConfig = {
    logging: boolean
}

export interface RootState {
    tasks: TaskState,
    socket: SocketState,
    theme: ThemeState
}

export const createStore = ({ logging }: StoreConfig) => {
    let middleware = [ ]
    if (logging) {
        middleware.push(createLogger())
    }

    return createReduxStore(
        combineReducers({
            tasks: tasks.reducer,
            socket: socket.reducer,
            theme: theme.reducer
        }),
        applyMiddleware(
            ...middleware
        )
    )
}

export default createStore
