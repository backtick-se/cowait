import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { useLocation } from 'react-router-dom'
import { FlexBox } from '..'
import { BreadcrumbWrapper, BreadcrumbLink } from './styled'


export type PathFragment = {
  path: string,
  name: string
}

/**
 * Split full path into incrementing traversable fragments
 * e.g. '/task/123/details' => ['/task', '/task/123', '/task/123/details']
 * @param {string} path - Full location path
 * @returns {PathFragment[]} - Traversable fragments, each going one level deeper
 */
const traversablePaths = (path: string): PathFragment[] => {
  if (path === '/') {
    return [{
      name: 'HOME',
      path: path
    }]
  }

  return path.split('/').slice(1).reduce<PathFragment[]>((acc, next) => {
    return acc.concat({
      name: next.toUpperCase(),
      path: `${acc.length ? acc[acc.length - 1].path : acc}/${next}`
    })
  }, [])
}

const createCrumbs = (location: string): React.ReactNode[] => {
  return traversablePaths(location).map((fragment, idx) =>
    <BreadcrumbWrapper key={idx}>
      {idx !== 0 && <FontAwesomeIcon icon="chevron-right" />}
      <BreadcrumbLink to={fragment.path}>{fragment.name}</BreadcrumbLink>
    </BreadcrumbWrapper>
  )
}

export default (() => {
  const location = useLocation()

  return <FlexBox>
    {createCrumbs(location.pathname)}
  </FlexBox>
}) as React.FC
