import styled from 'styled-components'
import { Link as RouterLink } from 'react-router-dom'

export const Link = styled(RouterLink)`
    color: #494ca2;
    text-decoration: none;

    &:visited,
    &:focus {
        color: #494ca2;
    }

    &:hover {
        color: lighten(#494ca2, 20%);
        text-decoration: underline;
    }
`

export default Link