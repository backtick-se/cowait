
import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import tasks from '../../../store/tasks'
import Button from '../../ui/Button'
import { RootState } from '../../../store'


type Props = {
  id: string,
  status: string
}

export default (({ id, status }) => {
  if (!['work', 'wait'].includes(status)) return null

  const dispatch = useDispatch()
  const taskActions = useSelector((state: RootState) => state.tasks.actions[id])
  
  const stopTask = () => {
    dispatch(tasks.actions.stop.request({ id }))
  }

  return <Button icon="stop" onClick={stopTask} {...taskActions?.stop}>Stop</Button>
}) as React.FC<Props>