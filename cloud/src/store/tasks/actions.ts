import { action, Action, createAsyncAction } from 'typesafe-actions'
import { TaskActionTypes } from "./types"

// the events have different shapes depending on different messages but have type and id in common
export type SocketTaskEvent = {
  type: string,
  id: string
}

const eventToAction = (taskEvent: SocketTaskEvent): Action => {
  const { type } = taskEvent
  const prefix = '@@'
  const [namespace, event] = type.split('/')
  const actionType = `${prefix}${namespace}/${event ? event.toUpperCase() : event}`

  return action(actionType, taskEvent)
}

export const clear = () => action(TaskActionTypes.CLEAR)
export const stop = createAsyncAction(
  TaskActionTypes.STOP_REQUEST,
  TaskActionTypes.STOP_SUCCESS,
  TaskActionTypes.STOP_FAILURE
)<{ id: string }, { id: string }, { id: string, error: string }>();
export const taskEvent = eventToAction