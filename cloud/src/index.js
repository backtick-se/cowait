import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import App from './components/App'
import PipeClientStore from './PipeClientStore'

const PORT = 1337


// figure out websocket uri from current location
let wsUri = `ws://${window.location.hostname}:${PORT}`
if (window.location.protocol === 'https:') {
    // if TLS is enabled, it means the agent is behind a reverse proxy.
    // the websocket should be available at /ws instead of port 1337
    // we should also use TLS.
    wsUri = `wss://${window.location.host}/ws`
}

const client = new PipeClientStore(wsUri)
client.connect()

render(
    <Provider store={client.store}>
        <App />
    </Provider>,
    document.getElementById('root')
)