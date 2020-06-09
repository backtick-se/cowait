import React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import App from './components/App'
import PipeClientStore from './PipeClientStore'
import { getWsUrl, updateToken } from './utils'

// import fa icon lib
import './components/fontawesome'

// update token from url
updateToken()

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