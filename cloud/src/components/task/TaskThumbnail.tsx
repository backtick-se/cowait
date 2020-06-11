import React from 'react'
import styled from 'styled-components'
import { FlexBox } from '../ui'
import { Task as TaskInterface } from '../../store/tasks/types'
import TaskStatus from '../task/TaskStatus'
import { TaskTitleWrapper, TaskHeaderLink, TaskImage, TaskTitle, TaskCreatedAt } from '../task/styled/Task'
import { formatDate } from '../../utils'


const ThumbnailWrapper = styled(FlexBox)`
  background: ${p => p.theme.colors.background.secondary};
  flex-direction: column;
  padding: 0.5rem 0.8rem;
  margin-bottom: 1rem;
  border-radius: ${p => p.theme.borderRadius};
`

export type TaskComponent = React.FC<TaskInterface>

export const TaskThumbnail: TaskComponent = ({ id, status, image, created_at }) => {
  return <ThumbnailWrapper>
    <TaskTitleWrapper>
      <TaskTitle>
        <TaskHeaderLink to={`/task/${id}`}>{id}</TaskHeaderLink>
        <TaskStatus status={status} />
      </TaskTitle>
      <TaskCreatedAt>{formatDate(created_at)}</TaskCreatedAt>
    </TaskTitleWrapper>
    <TaskImage>{image}</TaskImage>
  </ThumbnailWrapper>
}