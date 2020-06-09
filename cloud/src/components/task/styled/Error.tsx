import styled from 'styled-components'
import { ErrorBubble } from '../../ui'


export const ErrorOutput = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
    line-height: 1.5em;
`

export const ErrorBubblePadded = styled(ErrorBubble)`
    margin: 0 1rem;
`