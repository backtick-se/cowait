import { action } from 'typesafe-actions'
import { SocketActionTypes } from "./types"

export const connecting = () => action(SocketActionTypes.CONNECTING)
export const connected = () => action(SocketActionTypes.CONNECTED)
export const error = (error: string) => action(SocketActionTypes.ERROR, error)
export const closed = () => action(SocketActionTypes.CLOSED)