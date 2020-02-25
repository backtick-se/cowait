import styled from 'styled-components'


export const TaskStatusLabel = styled.label`
    display: inline-block;
    color: ${p => p.theme.colors.status[p.status]};
    border: 1px solid ${p => p.theme.colors.status[p.status]};
    padding: 0.25em 0.5em;
    font-size: 0.8em;
    border-radius: 0.3em;
    
    .fa {
        margin-right: 0.3em;
    }
`