import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { View } from '../ui'
import TaskList from '../task/TaskList'
import { Task } from '../../store/tasks/types'
import { TaskThumbnail } from '../task/TaskThumbnail'
import { Overview } from './styled'


const failedOnly = (task: Task): boolean =>
  task.status === 'fail'

const Home: React.FC = () => {
  return <View>
    <Overview>
      <div>
        <h2>Cowait Agent Dashboard</h2>
        <br />
        <p>Enjoying cowait? Be sure to give it a star on <a href="https://github.com/backtick-se/cowait">Github <FontAwesomeIcon icon={['fab', 'github-square']} />.</a></p>
        <br />
        <p>All contributions and feedback are greatly appreciated.</p>

      </div>
      <TaskList render={TaskThumbnail} title={"Recent tasks"} />
      <TaskList render={TaskThumbnail} title={"Recent failures"} predicate={failedOnly}/>
    </Overview>
  </View>
}

export default Home
