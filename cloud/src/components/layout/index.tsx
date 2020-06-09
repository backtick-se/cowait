import React from 'react'
import Navbar from '../ui/Navbar'
import Menu from '../ui/Menu'
import { HorizontalWrapper, ContentWrapper, VerticalWrapper } from './styled'


export const Layout: React.FC = ({ children }) => {
  return <HorizontalWrapper>
    <Menu />
    <VerticalWrapper>
      <Navbar />
      <ContentWrapper>
        {children}
      </ContentWrapper>
    </VerticalWrapper>
  </HorizontalWrapper>
}
