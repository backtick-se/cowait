import PipeClient from './PipeClient'
import { createStore } from './store'
import socket from './store/socket'

const DefaultStoreOptions = {
    logging: false
}


export class PipeClientStore extends PipeClient {
    constructor(uri, storeOptions = DefaultStoreOptions) {
        super(uri)
        const store = createStore(storeOptions)

        this.on('connecting', () => {
            store.dispatch(socket.actions.connecting())
        })
        this.on('connect', () => {
            store.dispatch({ type: 'clear' })
            store.dispatch(socket.actions.connected())
        })
        this.on('message', event => {
            store.dispatch(event)
        })
        this.on('error', error => {
            store.dispatch(socket.actions.error(error))
        })
        this.on('close', event => {
            store.dispatch(socket.actions.closed())
        })

        this.store = store
    }
}

export default PipeClientStore