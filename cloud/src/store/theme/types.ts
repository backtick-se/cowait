
import { UPDATE_THEME } from './reducer';
import { ThemeType } from '../../theme';

export type UPDATE_THEME = typeof UPDATE_THEME

export enum ThemeActionTypes {
  UPDATE = '@@theme/update',
}

export type ThemeState = {
  active: ThemeType
}

