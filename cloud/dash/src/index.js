import React from 'react'
import io from 'socket.io-client'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { ThemeProvider } from 'styled-components'
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import { createStore } from './store'

import { theme, GlobalStyle } from './theme'
import TaskView from './views/TaskView'
import TaskListView from './views/TaskListView'

function App() {
    return <ThemeProvider theme={theme}>
        <Router>
            <GlobalStyle />
            <Switch>
                <Route path="/task/:taskId">
                    <TaskView />
                </Route>
                <Route path="/">
                    <TaskListView />
                </Route>
            </Switch>
        </Router>
    </ThemeProvider>
}

const store = createStore({
    logging: false,
})

let socket = io('http://localhost:1338')
socket.on('msg', event => {
    store.dispatch(event)
})

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)