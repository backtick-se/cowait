import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { Menu, LogoContainer, MenuItem } from './styled'
import Logo from '../Logo'


export default (() =>
  <Menu>
    <LogoContainer>
      <Logo />
    </LogoContainer>
    <MenuItem to={"/"}>
      <FontAwesomeIcon icon="home" />
    </MenuItem>
    <MenuItem to={"/task"}>
      <FontAwesomeIcon icon="bars" />
    </MenuItem>
  </Menu>
) as React.FC