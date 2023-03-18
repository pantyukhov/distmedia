import { combineReducers } from 'redux';
import { FETCH_POSTS, RECEIVE_POSTS, SELECT_PUBLISHER, SELECT_READER, CONTENT_PUBLISHED } from './actions';

const initialState = {
  isFetching: false,
  items: [],
  type: null
};

export const posts = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_POSTS:
      return Object.assign({}, state, {
        isFetching: true,
      });
    case RECEIVE_POSTS:
      return Object.assign({}, state, {
        isFetching: false,
        items: state.items.concat(action.posts),
      });
    case SELECT_PUBLISHER:
      return Object.assign({}, state, {
        type: "publisher",
      });
    case SELECT_READER:
      return Object.assign({}, state, {
        type: "reader",
      });
    case CONTENT_PUBLISHED:
      return state;
    default:
      return state;
  }
};

export default combineReducers({ posts });
