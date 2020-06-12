import { DefaultTheme } from 'styled-components'


export enum ThemeType {
  Dark = 'Dark',
  Light = 'Light'
}

export interface ColorTheme {
  colors: {
      border: string,
      text: {
          [type: string]: string
      },
      link: {
          [type: string]: string
      },
      button: {
          [type: string]: string
      },
      menu: {
          [type: string]: string
      }
      background: {
          [type: string]: string
      },
      status: {
          [status: string]: string
      }
  }
}

export interface Theme extends ColorTheme, DefaultTheme {
  fonts: {
      [fontType: string]: string
  }
}
