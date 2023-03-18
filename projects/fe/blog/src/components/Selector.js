import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from '../helpers/withrouter';
import moment from 'moment';
import CircularProgress from 'material-ui/CircularProgress';
import Button from '@mui/material/Button';
import Divider from 'material-ui/Divider';
import Paper from 'material-ui/Paper';
import { getFullYear } from '../helpers/utilities';
import { height as headerHeight } from './Header';

const footerHeight = 50;
const contentStyle = {
  minHeight: `calc(100vh - ${headerHeight + footerHeight}px)`,
};
const paperStyle = { padding: 16 };

export class Selector extends PureComponent {
  _selectAsPublisher = () => {
    const { selectPublisher } = this.props;
    selectPublisher();
    const { navigate } = this.props.router;
    navigate('/publisher/feed');
  };

  _selectAsReader = () => {
    const { selectReader } = this.props;
    selectReader();
    const { navigate } = this.props.router;
    navigate('/reader/feed');
  };

  render() {
     const { selectPublisher } = this.props;
    return (
      <div>
        <h1>Please select one!</h1>
        <h2>I am a</h2>
        <Button onClick={this._selectAsReader} variant="contained">Just reading</Button>
        or 
        <Button onClick={this._selectAsPublisher} variant="contained">Publishing content</Button>
      </div>
    );
  }
}

const SelectorWithRouter = withRouter(Selector);
export default SelectorWithRouter;
