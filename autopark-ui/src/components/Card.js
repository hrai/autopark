import React, { Component } from 'react';
import '../App.css';
import { Card } from 'react-bootstrap';
import styled from 'styled-components';

const StyledCard = styled.div`
    box-shadow: 0 19px 19px rgba(0,0,0,0.30), 0 19px 19px rgba(0,0,0,0.22);

`

export default class HomeCard extends Component {
    constructor(props) {
        super(props);

    }
    render() {
        return (
                <Card
                bg={'light'}
                style={{ width: '18rem' }}
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