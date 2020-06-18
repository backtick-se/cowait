import styled from 'styled-components'
import { hex2Rgba } from '../../../utils'

type Props = {
    status: string
}

export const TaskStatusLabel = styled.label<Props>`
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0.25em 0.5em;
    color: ${p => p.theme.colors.status[p.status]};
    /* border: 1px solid ${p => p.theme.colors.status[p.status]}; */
    font-size: 0.5em;
    border-radius: ${p => p.theme.borderRadius};
    background: ${p => hex2Rgba(p.theme.colors.status[p.status || 'work'], 0.2)};
    
    span {
        margin-left: 0.5em;
    }

    svg {
        font-size: 1em;
    }
`