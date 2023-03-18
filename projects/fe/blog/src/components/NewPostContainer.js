import { connect } from 'react-redux';
import { publishContent } from '../redux/actions';
import NewPost from './NewPost';

const mapStateToProps = state => {
//  const { posts: { isFetching, items } } = state;
  return {
    // isLoading: isFetching,
    // posts: items,
  };
};

const mapDispatchToProps = dispatch => ({
  publishContent: (title, description, content) => dispatch(publishContent(title, description, content))
});

const wrapper = connect(mapStateToProps, mapDispatchToProps);
const NewPostContainer = wrapper(NewPost);
export default NewPostContainer;
