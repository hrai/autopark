import React, {Component} from 'react';
import '../App.css';
import {Card} from 'react-bootstrap';

export default class HomeCard extends Component {
  render() {
    return (
      <Card
        bg={'light'}
        style={{width: '18rem'}}
        className="cardStyle"
      >
        <Card.Header> {this.props.header} </Card.Header>
        <Card.Body>
          <Card.Title> {this.props.title} </Card.Title>
          <Card.Text>
            {this.props.content}
          </Card.Text>
        </Card.Body>
      </Card>
    );
  }
}
