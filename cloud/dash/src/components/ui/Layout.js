import React from 'react'
import styled from 'styled-components'

export const Bubble = styled.div`
    padding: 1rem;
    border-radius: 0.3rem;
    margin-bottom: 0.5rem;

    background-color: #fff;
    color: #222;

    h4 {
        font-size: 1.1rem;
        font-weight: bold;
        padding-bottom: 0.3rem;
    }
`

export const Header = styled.nav`
    background-color: #494ca2;
    color: #fff;

    padding: 0.5rem 1rem;
`

export const Wrapper = styled.div`
`

export const Content = styled.div`
    padding: 0.5rem;
`

export function View({ title, children }) {
    return <Wrapper>
        <Header>
            <h1>{title}</h1>
        </Header>
        <Content>
            {children}
        </Content>
    </Wrapper>
}

export const CodeBlock = styled.pre`
    font-family: ${p => p.theme.fonts.monospace};
`