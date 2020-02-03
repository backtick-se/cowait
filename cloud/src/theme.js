import { createGlobalStyle } from 'styled-components'

export const theme = {
    fonts: {
        normal: 'Oxygen',
        monospace: 'Nanum Gothic Coding',
    },

    colors: {
        text: '#ffffff',
        background: '#e3e7f1',

        status: {
            wait: '#999999',
            work: '#42b883',
            done: '#347474',
            fail: '#c70d3a',
            stop: '#ed5107',
        },
    },
}

export const GlobalStyle = createGlobalStyle`
    html {
        box-sizing: border-box;
        font-size: 16px;
    }

    *, *:before, *:after {
        box-sizing: inherit;
    }

    body {
        background-color: ${p => p.theme.colors.background};
    }

    body, h1, h2, h3, h4, h5, h6, p, ol, ul {
        margin: 0;
        padding: 0;

        font-weight: normal;
        font-family: ${p => p.theme.fonts.normal};
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


export default theme