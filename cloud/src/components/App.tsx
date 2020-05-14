import React from 'react'
import { ThemeProvider } from 'styled-components'
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'

import { theme, GlobalStyle } from '../theme'
import TaskView from './task/TaskView'
import TaskListView from './task/TaskListView'
import ErrorBoundary from './ui/ErrorBoundary'

import SocketOverlay from './ui/SocketOverlay'


export function App() {
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

export default App