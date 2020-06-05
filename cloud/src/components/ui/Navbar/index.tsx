import React from 'react'
import { Navbar } from './styled'
import ThemePicker from '../ThemePicker'
import Breadcrumbs from '../Breadcrumbs'
import SocketStatus from '../SocketStatus'
import { FlexBox } from '../FlexBox'


export default (() =>
  <Navbar>
    <Breadcrumbs />
    <FlexBox alignItems="center">
      <ThemePicker />
      <SocketStatus />
    </FlexBox>
  </Navbar>
) as React.FC