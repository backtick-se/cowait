
import styled from 'styled-components'

type Props = {
    minHeight?: number,
    maxHeight?: number
}

export const LogOutput = styled.pre<Props>`
    font-family: ${p => p.theme.fonts.monospace};
    color: ${p => p.theme.colors.text.secondary};
    line-height: 1.25em;
`

export const LogContainer = styled.div<Props>`
    padding: 1rem;
    background-color: ${p => p.theme.colors.background.terminal};
    border: 1px solid ${p => p.theme.colors.border};
    border-radius: ${p => p.theme.borderRadius};
    overflow: auto;
    min-height: ${p => p.minHeight || 6}rem;
    max-height: ${p => p.maxHeight || 12}rem;
`