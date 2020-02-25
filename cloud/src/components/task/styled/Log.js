
import styled from 'styled-components'


export const LogOutput = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
    color: white;
    line-height: 1.25em;
`

export const LogContainer = styled.div`
    padding: 0.5rem;
    background-color: #222;
    border-radius: 0.3rem;
    overflow: auto;
    min-height: ${p => p.minHeight || 6}rem;
    max-height: ${p => p.maxHeight || 12}rem;
`