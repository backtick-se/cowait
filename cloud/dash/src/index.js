import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware, combineReducers } from 'redux'
import { createLogger } from 'redux-logger'
import { useParams, Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import tasks from './store/tasks'
import io from 'socket.io-client'

import TaskList from './components/TaskList'
import Task from './components/task/Task'

function TaskView({ }) {
    let { taskId } = useParams();
    return <Task id={taskId} />
}

function App() {
    return <Router>
        <Switch>
            <Route path="/task/:taskId">
                <TaskView />
            </Route>
            <Route path="/">
                <TaskList />
            </Route>
        </Switch>
    </Router>
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