import { connect } from 'react-redux';
import { selectPublisher, selectReader } from '../redux/actions';
import Selector from './Selector';

const mapStateToProps = state => {
//  const { posts: { isFetching, items } } = state;
  return {
    // isLoading: isFetching,
    // posts: items,
  };
};

const mapDispatchToProps = dispatch => ({
  selectPublisher: () => dispatch(selectPublisher()),
  selectReader: () => dispatch(selectReader())
});

const wrapper = connect(mapStateToProps, mapDispatchToProps);
const SelectorContainer = wrapper(Selector);
export default SelectorContainer;
