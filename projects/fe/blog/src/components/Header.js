import React, { PureComponent } from 'react';
import Button from '@mui/material/Button';
import PropTypes from 'prop-types';
import { withRouter } from '../helpers/withrouter';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import ArrowBack from 'material-ui/svg-icons/navigation/arrow-back';

export const height = 64;

export class Header extends PureComponent {


  _handleClick = () => {
    const { navigate } = this.props.router;
    navigate('/');
  };

  render() {
    const { location: { pathname } } = this.props.router;
    const isPost = pathname.indexOf('/posts/') !== -1;
 
    return (
      <AppBar
        title="Euryale"
        iconElementLeft={
          isPost ? (
            <IconButton onClick={this._handleClick}>
              <ArrowBack />
            </IconButton>
          ) : null
        }
        iconElementRight={<Button onClick={this._handleClick} variant="text">Reset</Button>}
        showMenuIconButton={isPost}
        style={{ textAlign: 'center' }}
      />
    );
  }
}

const HeaderWithRouter = withRouter(Header);
export default HeaderWithRouter;
