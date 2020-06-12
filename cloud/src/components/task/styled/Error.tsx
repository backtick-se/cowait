import styled from 'styled-components'
import { ErrorBubble } from '../../ui'
import { hex2Rgba } from '../../../utils'

export const ErrorOutput = styled(ErrorBubble)`
    font-family: ${p => p.theme.fonts.monospace};
    line-height: 1.5em;
    white-space: break-spaces;
    background: ${p => p.theme.colors.background.terminal};
    color: ${p => hex2Rgba(p.theme.colors.status['fail'], 1)};
    border: 1px solid ${p => p.theme.colors.border};
`
