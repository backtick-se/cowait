import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { ThemeProvider } from 'styled-components'
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import { createStore } from './store'

import { theme, GlobalStyle } from './theme'
import TaskView from './views/TaskView'
import TaskListView from './views/TaskListView'
import ErrorBoundary from './ErrorBoundary'

import PipeClient from './PipeClient'
import socket from './store/socket'
import SocketOverlay from './components/SocketOverlay'

function App() {
    return <ThemeProvider theme={theme}>
        <Router>
            <GlobalStyle />
            <ErrorBoundary>
                <SocketOverlay>
                    <Switch>
                        <Route path="/task/:taskId">
                            <TaskView />
                        </Route>
                        <Route path="/">
                            <TaskListView />
                        </Route>
                    </Switch>
                </SocketOverlay>
            </ErrorBoundary>
        </Router>
    </ThemeProvider>
}

const store = createStore({
    logging: false,
})

let wsUri = `ws://${window.location.hostname}:1337`
if (window.location.protocol === 'https:') {
    // if TLS is enabled, it means the agent is behind a reverse proxy.
    // the websocket should be available at /ws instead of port 1337
    // we should also use TLS.
    wsUri = `wss://${window.location.host}/ws`
}

let client = new PipeClient(wsUri)
client.on('connecting', () => {
    store.dispatch(socket.actions.connecting())
})
client.on('connect', () => {
    console.log('connected. clear store')
    store.dispatch({ type: 'clear' })
    store.dispatch(socket.actions.connected())
})
client.on('message', event => {
    store.dispatch(event)
})
client.on('error', error => {
    console.log('error', error)
    store.dispatch(socket.actions.error(error))
})
client.on('close', event => {
    console.log('closed', event)
    store.dispatch(socket.actions.closed())
})
client.connect()

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)