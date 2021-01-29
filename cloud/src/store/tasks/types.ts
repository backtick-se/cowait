export enum TaskActionTypes {
  INIT = '@@task/INIT',
  STATUS = '@@task/STATUS',
  RETURN = '@@task/RETURN',
  FAIL = '@@task/FAIL',
  STATE = '@@task/STATE',
  LOG = '@@task/LOG',
  CLEAR = '@@task/CLEAR',
  STOP_REQUEST = '@@task/STOP_REQUEST',
  STOP_SUCCESS = '@@task/STOP_SUCCESS',
  STOP_FAILURE = '@@task/STOP_FAILURE'
}

export interface Task {
  cpu: string,
  created_at: string,
  env: object,
  error: string,
  id: string,
  image: string,
  inputs: object,
  memory: string,
  meta: object,
  name: string,
  owner: string,
  parent: string | null,
  ports: object,
  result?: object,
  routes: object,
  status: string,
  upstream: string,
  sub_tasks: string[],
  state: object,
}

export interface TaskState {
  order: string[],
  items: {
    [task_id: string]: Task
  },
  logs: {
    [task_id: string]: string
  },
  actions: {
    [task_id: string]: {
      [action: string]: {
        error?: string,
        success?: boolean,
        loading: boolean
      }
    }
  }
}
