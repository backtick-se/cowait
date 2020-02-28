import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import App from './components/App'
import PipeClientStore from './PipeClientStore'

const PORT = 1337

export function getWsUrl() {
    // figure out websocket uri from current location
    let wsProto = window.location.protocol === 'https:' ? 'wss' : 'ws'

    // if we are on port 80, it means the agent is behind a reverse proxy.
    // the websocket should be available at /ws
    if (window.location.port === '') {
        return `${wsProto}://${window.location.host}/ws`
    }

    // default to window url on port 1337
    return `${wsProto}://${window.location.hostname}:${PORT}`
}

// connect websocket client
const client = new PipeClientStore(getWsUrl())
client.connect()

// render page
render(
    <Provider store={client.store}>
        <App />
    </Provider>,
    document.getElementById('root')
)