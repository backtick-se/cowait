import { action } from 'typesafe-actions'
import { TaskActionTypes } from "./types"
import { AnyAction } from 'redux';

const convertEventToAction = (action: AnyAction): AnyAction => {
  const prefix = '@@'
  const [namespace, event] = action.type.split('/')

  const a = {
    ...action,
    type: `${prefix}${namespace}/${event.toUpperCase()}`
  }

  console.log('action', a);
  return a
} 
export const clear = () => action(TaskActionTypes.CLEAR)
export const taskEvent = convertEventToAction