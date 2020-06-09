import styled from 'styled-components'

type Props = {
    status: string
}

export const TaskStatusLabel = styled.label<Props>`
    display: inline-block;
    padding: 0.25em 0.5em;
    color: ${p => p.theme.colors.status[p.status]};
    border: 1px solid ${p => p.theme.colors.status[p.status]};
    font-size: 0.8em;
    border-radius: 0.3em;
    
    .fa {
        margin-right: 0.3em;
    }
`