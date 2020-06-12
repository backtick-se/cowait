import { all, call, fork, put, takeEvery, StrictEffect } from 'redux-saga/effects'
import { callApi, constructApiUri } from '../../utils'
import { stop } from './actions'


function* watchFetchRequest() {
  yield takeEvery(stop.request, handleStop)
}

function* handleStop(action: ReturnType<typeof stop.request>): Generator<StrictEffect> {
  const { id } = action.payload
  const data = {
    'task_id': action.payload.id
  }
  
  try {
    yield call(callApi, 'POST', constructApiUri('rpc/destroy'), data)
    yield put(stop.success({ id }))
  } catch (error) {
    yield put(stop.failure({ id, error }))
  }
}

function* tasksSaga() {
  yield all([fork(watchFetchRequest)])
}

export default tasksSaga