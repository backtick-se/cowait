import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import App from './components/App'
import PipeClientStore from './PipeClientStore'


export function getWsUrl() {
    // figure out websocket uri from current location
    let wsProto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    return `${wsProto}://${window.location.host}/ws`
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