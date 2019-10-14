import { createGlobalStyle } from 'styled-components'

export const theme = {
    fonts: {
        normal: 'Oxygen',
        monospace: 'Nanum Gothic Coding',
    },

    colors: {
        status: {
            wait: '#999999',
            work: '#ffad13',
            done: 'green',
            fail: 'red',
            stop: 'orange',
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

    body, h1, h2, h3, h4, h5, h6, p, ol, ul {
        margin: 0;
        padding: 0;
        font-weight: normal;
        font-family: ${p => p.theme.fonts.normal};
    }

    body {
        padding: 0.5rem;
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
`


export default theme