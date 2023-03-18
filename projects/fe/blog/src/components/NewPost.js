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
import TextField from '@mui/material/TextField';

const footerHeight = 50;
const contentStyle = {
  minHeight: `calc(100vh - ${headerHeight + footerHeight}px)`,
};
const paperStyle = { padding: 16 };

export class Selector extends PureComponent {
  _selectAsPublisher = () => {
    const { publishContent } = this.props;
    publishContent();
    const { navigate } = this.props.router;
    navigate('/publisher/feed');
  };

  render() {
     //const { selectPublisher } = this.props;
    return (
      <div>
        <h1>Writing a new Post!</h1>
        <TextField
          required
          id="outlined-required"
          label="Title"
        />
        <TextField
          required
          id="outlined-required"
          label="Description"
        />
         <TextField
          id="outlined-multiline-static"
          label="Multiline"
          multiline
          rows={15}
          defaultValue="Content"
        />
        <Button onClick={this._selectAsPublisher} variant="contained">Submit content</Button>
      </div>
    );
  }
}

const SelectorWithRouter = withRouter(Selector);
export default SelectorWithRouter;
