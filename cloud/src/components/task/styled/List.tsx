import styled from 'styled-components'
import { lighten } from 'polished'


export const TaskListEmptyItem = styled.div`
    display: flex;
    align-items: center;
    justify-content: center;
    color: ${p => p.theme.colors.text.secondary};
    font-size: 0.8rem;
    background: ${p => lighten(0.1, p.theme.colors.background.secondary)};
    border-radius: ${p => p.theme.borderRadius};
    padding: 0.5rem;
`