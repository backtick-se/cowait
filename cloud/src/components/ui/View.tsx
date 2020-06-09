import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'
import { Header, Content } from './Layout'

const HeaderLink = styled(Link)`
    color: #ffffff;
    text-decoration: none;

    &:hover,
    &:focus,
    &:visited,
    &:active {
        color: #ffffff;
    }
`

type Props = {
    title: string
}

export const View: React.FC<Props> = ({ title, children }) => {
    return <div>
        <Header>
            <h1>
                <i className="fa fa-list-ol" />
                <HeaderLink to="/">{title}</HeaderLink>
            </h1>
        </Header>
        <Content>
            {children}
        </Content>
    </div>
}