import styled from 'styled-components'
import { ErrorBubble } from '../../ui'


export const ErrorOutput = styled(ErrorBubble)`
    font-family: ${p => p.theme.fonts.monospace};
    line-height: 1.5em;
    white-space: break-spaces;
`
