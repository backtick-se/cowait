import { ThemeState, ThemeActionTypes } from './types'
import { Reducer } from 'redux'
import { loadFromLocalStorage } from '../../utils'
import { ThemeType } from '../../theme'


export const UPDATE_THEME = 'update_theme'
const LOCAL_STORAGE_KEY = 'agent-dashboard-theme'

const initialState: ThemeState = {
    active: loadFromLocalStorage(LOCAL_STORAGE_KEY) || ThemeType.Dark
}

const reducer: Reducer<ThemeState> = (state = initialState, action) => {
    switch(action.type) {
    case ThemeActionTypes.UPDATE:
        return {
            ...state,
            active: action.payload
        }
    default:
        return state
    }
}

export default reducer
