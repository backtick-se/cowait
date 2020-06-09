import React from 'react'

import { availableThemes, ThemeType } from '../../../theme'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '../../../store'
import theme from '../../../store/theme'
import { ThemeIcon, ThemePicker } from './styled'


const ThemeButton: React.FC<{ name: string, active: boolean, color: string }> = ({ name, ...rest }) => {
  const dispatch = useDispatch()

  const onClick = (_: any) => {
    dispatch(theme.actions.updateTheme(name as ThemeType))
  }

  return <ThemeIcon onClick={onClick} {...rest} />
}

export default (() => {
  const themes = availableThemes()
  const currentTheme = useSelector((state: RootState) => state.theme.active)

  const buttons = Object.keys(themes).map((theme, idx) =>
    <ThemeButton
      key={idx}
      name={theme}
      active={theme === currentTheme}
      color={themes[theme].colors.background.primary}
    />
  )

  return <ThemePicker>
    {buttons}
  </ThemePicker>
}) as React.FC
