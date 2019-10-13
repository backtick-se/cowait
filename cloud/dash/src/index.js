import React from 'react'
import styled from 'styled-components'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, combineReducers } from 'redux'
import { createLogger } from 'redux-logger'
import tasks from './store/tasks'
import io from 'socket.io-client'

import TaskList from './components/TaskList'

function App() {
    return <TaskList />
}

const logger = createLogger()

const store = createStore(
    combineReducers({
        tasks: tasks.reducer,
    }),
    applyMiddleware(logger)
)

let socket = io('http://localhost:1338')
socket.on('msg', event => {
    console.log(event)
    store.dispatch(event)
})

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)