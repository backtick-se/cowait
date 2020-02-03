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

function App() {
    return <ThemeProvider theme={theme}>
        <Router>
            <GlobalStyle />
            <ErrorBoundary>
                <Switch>
                    <Route path="/task/:taskId">
                        <TaskView />
                    </Route>
                    <Route path="/">
                        <TaskListView />
                    </Route>
                </Switch>
            </ErrorBoundary>
        </Router>
    </ThemeProvider>
}

const store = createStore({
    logging: false,
})

let client = new PipeClient('ws://localhost:1337')
client.on('connect', () => {
    console.log('clear store')
    store.dispatch({ type: 'clear' })
})
client.on('message', event => {
    store.dispatch(event)
})
client.connect()

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
)