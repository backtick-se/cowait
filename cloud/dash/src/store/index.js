import { 
    createStore as createReduxStore, 
    applyMiddleware, 
    combineReducers, 
} from 'redux'
import { createLogger } from 'redux-logger'
import tasks from './tasks'

export function createStore({ logging }) {
    let middleware = [ ]
    if (logging) {
        middleware.push(createLogger())
    }

    return createReduxStore(
        combineReducers({
            tasks: tasks.reducer,
        }),
        applyMiddleware(
            ...middleware
        )
    )
}

export default createStore  