import React from 'react'
import { Navbar } from './styled'
import ThemePicker from '../ThemePicker'
import Breadcrumbs from '../Breadcrumbs'

export default (() =>
  <Navbar>
    <Breadcrumbs />
    <ThemePicker />
  </Navbar>
) as React.FC