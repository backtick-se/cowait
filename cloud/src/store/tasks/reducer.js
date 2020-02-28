const DefaultState = {
    order: [ ],
    items: { },
    logs: { },
}

// task messages
const TASK_INIT = 'task/init'
const TASK_STATUS = 'task/status'
const TASK_RETURN = 'task/return'
const TASK_FAIL = 'task/fail'
const TASK_LOG = 'task/log'


export function tasks(state, action) {
    if (typeof(state) == 'undefined') {
        return DefaultState
    }

    switch(action.type) {
    case TASK_INIT: {
        const { task } = action
        if (!task.parent) {
            return {
                ...state,
                order: [ task.id, ...state.order ],
                items: {
                    ...state.items,
                    [task.id]: {
                        ...task,
                        children: [ ],
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
                        children: [ ],
                    },
                    [task.parent]: {
                        ...parent,
                        children: [ ...parent.children, task.id ],
                    },
                },
                logs: {
                    ...state.logs,
                    [task.id]: task.log || '',
                },
            }
        }
    }

    case TASK_STATUS: {
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

    case TASK_LOG: {
        const { id, data } = action
        return {
            ...state,
            logs: {
                ...state.logs,
                [id]: (state.logs[id] || '') + data,
            },
        }
    }

    case TASK_RETURN: {
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

    case TASK_FAIL: {
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

    case 'clear': {
        return DefaultState
    }
        
    default:
        return state
    }
}

export default tasks