import styled from 'styled-components'
import { Link } from '../../ui'


export const LinkWrapper = styled.span`
    display: flex;
    padding: 0.25em 0;
    align-items: center;

    ${Link} {
        margin-right: 0.5em;
        font-family: ${p => p.theme.fonts.monospace};
    }
`