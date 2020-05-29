import { action } from 'typesafe-actions'
import { TaskActionTypes } from "./types"
import { AnyAction } from 'redux'

const conformActionType = (action: AnyAction): AnyAction => {
  const prefix = '@@'
  const [namespace, event] = action.type.split('/')

  return {
    ...action,
    type: `${prefix}${namespace}/${event ? event.toUpperCase() : event}`
  }
}

export const clear = () => action(TaskActionTypes.CLEAR)
export const taskEvent = conformActionType