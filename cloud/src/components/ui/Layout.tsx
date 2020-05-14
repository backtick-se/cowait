import styled from 'styled-components'

type Props = {
    shadow?: string
}

export const Bubble = styled.div<Props>`
    padding: 1rem;
    border-radius: 0.3rem;
    margin-bottom: 0.5rem;

    background-color: #fff;
    color: #222;

    box-shadow: ${p => p.shadow || '0px 0px 3px rgba(0,0,0,0.05)'};

    h4 {
        font-size: 1.1rem;
        padding-bottom: 0.3rem;
    }
`

export const ErrorBubble = styled(Bubble)`
    color: white;
    background-color: ${p => p.theme.colors.status.fail};
`

export const Header = styled.nav`
    background-color: #494ca2;
    color: #fff;

    padding: 1rem 1.5rem;

    .fa {
        margin-right: 0.5em;
    }
`

export const Content = styled.div`
    padding: 0.5rem;
`