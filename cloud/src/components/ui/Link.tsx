import styled from 'styled-components'
import { Link as RouterLink } from 'react-router-dom'

export const Link = styled(RouterLink)`
    text-decoration: none;

    &:hover {
        text-decoration: underline;
    }
`

export default Link