import { darken } from 'polished'
import colors from './colors.json'
import { ColorTheme } from '../types'


export const theme: ColorTheme = {
    colors: {
        border: colors.grayscale5,
        text: {
            primary: colors.grayscale0,
            secondary: colors.grayscale3,
            lowkey: colors.grayscale4
        },
        link: {
            primary: darken(0.05, colors.purple),
            hover: colors.purple
        },
        button: {
            background: colors.purple,
            color: colors.grayscale0
        },
        menu: {
            primary: colors.grayscale0,
            hover: colors.purple
        },
        background: {
            primary: colors.darkestGreen,
            secondary: colors.darkGreen,
            terminal: colors.darkestGreen
        },

        status: {
            wait: colors.grayscale1,
            work: colors.blue,
            done: colors.green,
            fail: colors.red,
            stop: colors.yellow
        }
    },
}

export default theme
