import { action } from 'typesafe-actions'
import { ThemeActionTypes } from "./types"
import { ThemeType } from '../../theme/types'

export const updateTheme = (theme: ThemeType) => action(ThemeActionTypes.UPDATE, theme)