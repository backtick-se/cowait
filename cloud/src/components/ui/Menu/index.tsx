import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { Menu, Logo, MenuItem } from './styled'


export default (() =>
  <Menu>
    <Logo>
      <img src="cw_logo.png" />
    </Logo>
    <MenuItem to={"/"}>
      <FontAwesomeIcon icon="home" />
    </MenuItem>
    <MenuItem to={"/task"}>
      <FontAwesomeIcon icon="bars" />
    </MenuItem>
  </Menu>
) as React.FC