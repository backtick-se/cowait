import React from 'react'
import { ThemeProvider } from 'styled-components'
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import { useSelector } from 'react-redux'

import { GlobalStyle, selectTheme } from '../theme'
import Home from './home'
import TaskView from './task/TaskView'
import TaskListView from './task/TaskListView'
import ErrorBoundary from './ui/ErrorBoundary'
import { RootState } from '../store'
import { Layout } from './layout'


export function App() {
    const type = useSelector((state: RootState) => state.theme.active)
    const theme = selectTheme(type)

    return <ThemeProvider theme={theme}>
        <Router>
            <GlobalStyle />
            <Layout>
                <ErrorBoundary>
                    <Switch>
                        <Route path="/task/:taskId" component={TaskView} />
                        <Route path="/task" component={TaskListView} />
                        <Route path="/" component={Home} />
                    </Switch>
                </ErrorBoundary>
            </Layout>
        </Router>
    </ThemeProvider>
}

export default App