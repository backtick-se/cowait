import { createGlobalStyle, DefaultTheme } from 'styled-components'


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

const defaultTheme = {
    borderRadius: '0.2rem',
    fonts: {
        normal: 'Heebo',
        header: 'Heebo',
        monospace: 'IBM Plex Mono',
    }
}

export const availableThemes = () =>
    Object.keys(ThemeType).reduce((acc, theme) => {
        const colorTheme = require(`./${theme.toLowerCase()}`)

        return {
            ...acc,
            [theme]: {
                ...defaultTheme,
                ...colorTheme.theme
            }
        }
    }, {} as { [themeType: string]: Theme })

export const selectTheme = (type: ThemeType): Theme => {
    const themes = availableThemes()
    
    return themes[type]
}

export const GlobalStyle = createGlobalStyle<{ theme: Theme }>`
    * {
        font-family: ${p => p.theme.fonts.normal};
    }

    html {
        box-sizing: border-box;
        font-size: 16px;
    }

    *, *:before, *:after {
        box-sizing: inherit;
    }

    body {
        background-color: ${p => p.theme.colors.background.primary};
    }

    h1, h2, h3, h4, h5 {
        font-family: ${p => p.theme.fonts.header};
        color: ${p => p.theme.colors.text.primary};
        margin: 0;
        padding: 0;
    }

    body, p, ol, ul {
        margin: 0;
        padding: 0;

        font-weight: normal;
        color: ${p => p.theme.colors.text.primary};
    }

    a {
        transition: 0.3s;
        color: ${p => p.theme.colors.text.primary};
        text-decoration: none;
        cursor: pointer;
        
        &:focus,
        &:visited,
        &:active {
            color: ${p => p.theme.colors.text.primary};
        }
      
        &:hover {
          color: ${p => p.theme.colors.link.hover};  
        }
    }

    ol, ul {
        list-style: none;
    }

    img {
        max-width: 100%;
        height: auto;
    }

    pre {
        margin: 0;
    }

    pre, 
    code,
    pre span,
    code span {
        margin: 0;
        font-family: ${p => p.theme.fonts.monospace};
    }
`
