import _ from 'lodash'
import React from 'react'
import { useSelector } from 'react-redux'
import { RootState } from '../../../store'
import DagreGraph from 'dagre-d3-react'
import styled from 'styled-components'

const DagStyle = styled.div`
    .nodes {
        fill: darkgray;
        cursor: pointer;
    }

    // status colors
    .nodes .work { fill: #82b332; }
    .nodes .done { fill: green; }
    .nodes .fail { fill: red; }
    .nodes .stop { fill: orange; }

    .nodes text {
        fill: white;
    }
    
    path {
        stroke: white;
        fill: white;
        stroke-width: 3px;
    }
`

type Props = {
    graph: TaskGraph
}

type TaskGraph = {
    [id: string]: TaskNode,
}

type TaskNode = {
    id: string
    task: string
    depends_on: string[]
    task_id?: string
}

type d3Link = {
	source: string
	target: string
	class?: string
	label?: string
	config?: object
}

export const TaskGraph: React.FC<Props> = ({ graph }) => {
    const tasks = useSelector((state: RootState) => state.tasks.items)
    let nodes = _.map(graph, node => {
        if (node.task_id && tasks[node.task_id]) {
            let task = tasks[node.task_id]
            return {
                id: node.id,
                label: task.id,
                class: task.status,
            }
        }
        return {
            id: node.id,
            label: node.task,
            class: 'pending',
        }
    })
    let links: d3Link[] = []
    _.each(graph, node => {
        _.each(node.depends_on, edge => {
            links.push({
                source: edge,
                target: node.id,
            })
        })
    })
    return <DagStyle>
        <DagreGraph
            nodes={nodes}
            links={links}
            config={{
                rankdir: 'LR',
                align: 'UL',
                ranker: 'tight-tree'
            }}
            width='100%'
            height='500'
            animate={100}
            shape='rect'
            zoomable
            onNodeClick={(e: any) => console.log(e)}
        />
    </DagStyle>
}

export default TaskGraph