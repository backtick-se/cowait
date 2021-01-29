import _ from 'lodash'
import { TaskState, TaskActionTypes } from './types'
import { Reducer } from 'redux'

const initialState: TaskState = {
    order: [],
    items: {},
    logs: {},
    actions: {}
}

// Prepend an item to a set. If replace is true and the item already exists,
// it will be moved to the front. Otherwise, the set is returned without change.
function setPrepend(list: string[], item: string, replace: boolean = true) {
    const idx = _.indexOf(list, item)
    if (idx > 0) {
        if (replace) {
            return [
                item, 
                ...list.slice(0, idx), 
                ...list.slice(idx+1),
            ]
        } else {
            return list
        }
    }
    return [ item, ...list ]
}


const reducer: Reducer<TaskState> = (state = initialState, action) => {
    switch(action.type) {
    case TaskActionTypes.INIT: {
        const { task } = action.payload
        if (!task.parent) {
            return {
                ...state,
                order: setPrepend(state.order, task.id),
                items: {
                    ...state.items,
                    [task.id]: {
                        ...task,
                        sub_tasks: [ ],
                    },
                },
                logs: {
                    ...state.logs,
                    [task.id]: task.log || '',
                },
            }
        }
        else {
            const parent = state.items[task.parent]
            return {
                ...state,
                items: {
                    ...state.items,
                    [task.id]: {
                        ...task,
                        sub_tasks: [ ],
                    },
                    [task.parent]: {
                        ...parent,
                        sub_tasks: [ ...parent.sub_tasks, task.id ],
                    },
                },
                logs: {
                    ...state.logs,
                    [task.id]: task.log || '',
                },
            }
        }
    }

    case TaskActionTypes.STATUS: {
        const { id, status } = action.payload
        const item = state.items[id]
        if (!item) {
            console.log('unknown task', id)
            return state
        }
        if (item.status === 'fail' || item.status === 'done') {
            console.log('cant change status on', id, 'its already', item.status)
            return state
        }
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    status,
                },
            },
        }
    }

    case TaskActionTypes.LOG: {
        const { id, data } = action.payload
        return {
            ...state,
            logs: {
                ...state.logs,
                [id]: (state.logs[id] || '') + data,
            },
        }
    }

    case TaskActionTypes.RETURN: {
        const { id, result } = action.payload
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    result,
                },
            },
        }
    }

    case TaskActionTypes.FAIL: {
        const { id, error } = action.payload
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    error,
                },
            },
        }
    }

    case TaskActionTypes.STATE: {
        const { id, state: taskState } = action.payload
        return {
            ...state,
            items: {
                ...state.items,
                [id]: {
                    ...state.items[id],
                    state: taskState,
                },
            },
        }
    }

    case TaskActionTypes.CLEAR: {
        return initialState
    }

    case TaskActionTypes.STOP_REQUEST: {
        const { id } = action.payload
        return {
            ...state,
            actions: {
                ...state.actions,
                [id]: {
                    ...state.actions[id],
                    'stop': {
                        loading: true,
                        error: undefined
                    }
                }
            }
        }
    }

    case TaskActionTypes.STOP_FAILURE: {
        const { id, error } = action.payload
        return {
            ...state,
            actions: {
                ...state.actions,
                [id]: {
                    ...state.actions[id],
                    'stop': {
                        loading: false,
                        error: error
                    }
                }
            }
        }
    }

    case TaskActionTypes.STOP_SUCCESS: {
        const { id } = action.payload
        return {
            ...state,
            actions: {
                ...state.actions,
                [id]: {
                    ...state.actions[id],
                    'stop': {
                        loading: false,
                        error: undefined
                    }
                }
            }
        }
    }
        
    default:
        return state
    }
}

export default reducer