import _ from 'lodash'
import { TaskState, TaskActionTypes } from './types'
import { Reducer } from 'redux'

const initialState: TaskState = {
    order: [],
    items: {},
    logs: {}
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
        const { task } = action
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
        const { id, status } = action
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
        const { id, data } = action
        return {
            ...state,
            logs: {
                ...state.logs,
                [id]: (state.logs[id] || '') + data,
            },
        }
    }

    case TaskActionTypes.RETURN: {
        const { id, result } = action
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
        const { id, error } = action
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

    case TaskActionTypes.CLEAR: {
        return initialState
    }
        
    default:
        return state
    }
}

export default reducer