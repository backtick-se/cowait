import { lighten } from 'polished'
import colors from './colors.json'
import { ColorTheme } from '../types'


export const theme: ColorTheme = {
    colors: {
        border: colors.grayscale1,
        text: {
            primary: colors.grayscale6,
            secondary: colors.grayscale4,
        },
        link: {
            primary: colors.purple,
            hover: lighten(0.1, colors.purple)
        },
        button: {
            background: colors.purple,
            color: colors.grayscale0
        },
        menu: {
            primary: colors.grayscale6,
            hover: colors.purple
        },
        background: {
            primary: colors.grayscale0,
            secondary: colors.white,
            terminal: colors.grayscale0
        },

        status: {
            wait: colors.grayscale3,
            work: colors.blue,
            done: colors.green,
            fail: colors.red,
            stop: colors.yellow
        }
    },
}

export default theme
