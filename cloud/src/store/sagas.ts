import { all, fork } from 'redux-saga/effects'
import tasks from './tasks'


export function* rootSaga() {
  yield all([fork(tasks.sagas)])
}