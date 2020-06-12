import React from 'react'
import styled from 'styled-components'

import StopButton from './StopButton'
import { Task } from '../../../store/tasks/types'
import { FlexBox } from '../../ui'


const ActionBar = styled(FlexBox)`
  > {
    &:first-child {
      margin-left: 1rem;
    }
  }
`

const TaskActionBar: React.FC<Task> = ({ id, status }) => {
  return <ActionBar>
    <StopButton id={id} status={status}/>
  </ActionBar>
}

export default TaskActionBar