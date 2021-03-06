import React from 'react';
import './App.css';
import Visits from '../src/components/Visits'
import Home from './Home';
import Uploader from '../src/components/Uploader'
import Summary from '../src/components/Summary'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import {Navbar, Nav} from 'react-bootstrap'

function App() {
  return (
    <Router>
      <div>
        <Navbar bg="light" expand="lg">
          <Navbar.Brand as={Link} to="/" >Plate Mates</Navbar.Brand>
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/visits">Visits</Nav.Link>
              <Nav.Link href="/uploader">Image Uploader</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>
      <div>
        <Switch>
          <Route path="/visits">
            <Visits />
          </Route>
          <Route path="/uploader">
            <Uploader />
          </Route>
          <Route path="/summary">
            <Summary />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
