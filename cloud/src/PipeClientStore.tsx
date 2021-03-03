import PipeClient from './PipeClient'
import { createStore, StoreConfig } from './store'

import socket from './store/socket'
import tasks from './store/tasks'
import { Store } from 'redux'

const defaultStoreConfig: StoreConfig = {
    logging: true // redux-logger
}

export class PipeClientStore extends PipeClient {
    store: Store
    constructor(uri: string, storeConfig = defaultStoreConfig) {
        super(uri)
        const store = createStore(storeConfig)

        this.on('connecting', () => {
            store.dispatch(socket.actions.connecting())
        })
        this.on('connect', () => {
            store.dispatch(tasks.actions.clear())
            store.dispatch(socket.actions.connected())
        })
        this.on('message', event => {
            store.dispatch(tasks.actions.taskEvent(event))
        })
        this.on('error', error => {
            store.dispatch(socket.actions.error(error))
        })
        this.on('close', _ => {
            store.dispatch(socket.actions.closed())
        })

        this.store = store
    }
}

export default PipeClientStore