import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useLocation } from 'react-router-dom'
import { FlexBox } from '..'
import { BreadcrumbWrapper, BreadcrumbLink } from './styled'
import { traversablePaths } from '../../../utils'


const createCrumbs = (location: string): React.ReactNode[] =>
  traversablePaths(location).map((fragment, idx) =>
    <BreadcrumbWrapper key={idx}>
      {idx !== 0 && <FontAwesomeIcon icon="chevron-right" />}
      <BreadcrumbLink to={fragment.path}>{fragment.name}</BreadcrumbLink>
    </BreadcrumbWrapper>
  )

export default (() => {
  const location = useLocation()

  return <FlexBox>
    {createCrumbs(location.pathname)}
  </FlexBox>
}) as React.FC
