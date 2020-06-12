import { 
    createStore as createReduxStore, 
    applyMiddleware,
    combineReducers
} from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import { createLogger } from 'redux-logger'
import createSagaMiddleware from 'redux-saga';

import tasks from './tasks'
import socket from './socket'
import theme from './theme'
import { TaskState } from './tasks/types'
import { SocketState } from './socket/types'
import { ThemeState } from './theme/types'
import { rootSaga } from './sagas';


export type StoreConfig = {
    logging: boolean
}

export interface RootState {
    tasks: TaskState,
    socket: SocketState,
    theme: ThemeState
}

export const createStore = ({ logging }: StoreConfig) => {
    let middleware = [ ]
    
    // redux console logger
    if (logging) {
        middleware.push(createLogger())
    }

    // sagas
    const sagaMiddleware = createSagaMiddleware()
    middleware.push(sagaMiddleware)

    const store = createReduxStore(
        combineReducers({
            tasks: tasks.reducer,
            socket: socket.reducer,
            theme: theme.reducer
        }),
        composeWithDevTools(
            applyMiddleware(
                ...middleware
            )
        )
    )

    sagaMiddleware.run(rootSaga)
    return store
}

export default createStore
