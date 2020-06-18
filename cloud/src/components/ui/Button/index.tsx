import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { IconName } from '@fortawesome/fontawesome-svg-core'
import { StyledButton } from './styled'


type Props = {
  icon?: string | string[] | null,
  loading?: boolean,
  onClick?: () => void
}

const Button: React.FC<Props> = ({ children, icon, onClick, loading }) => {
  return <StyledButton onClick={onClick} disabled={false}>
    {icon && <FontAwesomeIcon icon={icon as IconName} />}
    {children}
  </StyledButton>
}

export default Button