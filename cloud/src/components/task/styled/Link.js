import styled from 'styled-components'
import { Link } from '../../ui'


export const LinkWrapper = styled.span`
    display: block;
    padding: 0.25em 0;

    ${Link} {
        margin-right: 0.5em;
        font-family: ${p => p.theme.fonts.monospace};
    }
`