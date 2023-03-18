import React, { PureComponent } from 'react';
import {
  BrowserRouter as Router,
  Navigate,
  Route,
  Routes,
  Redirect
} from 'react-router-dom';
import { Provider } from 'react-redux';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Header from './Header';
import PostListContainer from './PostListContainer';
import PostContainer from './PostContainer';
import SelectorContainer from './SelectorContainer';
import NewPostContainer from './NewPostContainer';
import store from '../redux/store';

export default class App extends PureComponent {
  _redirectToHome() {
    return <Navigate to="/" />;
  }

  render() {
    return (
      <Provider store={store}>
        <MuiThemeProvider>
          <Router>
            <div>
              <Header />

              {/* content */}
              <Routes>
                <Route exact path="/" element={<SelectorContainer />} />
                <Route exact path="/publisher/feed" element={<PostListContainer />} />
                <Route exact path="/publisher/new" element={<NewPostContainer />} />
                <Route exact path="/reader/feed" element={<PostListContainer />} />
                <Route path="/posts/:id/:slug" element={<PostContainer />} />

                {/* catch-all redirects to home */}
                <Route path="*" element={<Navigate to="/" replace />}/>
              </Routes>
            </div>
          </Router>
        </MuiThemeProvider>
      </Provider>
    );
  }
}
