import React, { Component } from 'react';
import styled from 'styled-components';
import Card from '../src/components/Card'
import { CardDeck, Button } from 'react-bootstrap';
import './App.css';


const Title = styled.h2`
  margin: 8px;
  padding-top: 1%;
  padding-left: 2%;
  text-align: center;
`;

const Subtitle = styled.h5`
  text-align: center;
  font-weight:normal;
  padding:10px;
`


export default class Home extends Component {
  render() {
    const firstCardHeader = "Step 1";
    const firstCardTitle = "Take picture";
    const firstCardContent = "Take a picture of your vehicle and make sure the number plate is visible.";
    
    const secondCardHeader = "Step 2";
    const secondCardTitle = "Upload Picture";
    const secondCardContent = "Upload your image for pre-processing & evaluation.";

    const thirdCardHeader = "Step 3";
    const thirdCardTitle = "Number plate recognized!";
    const thirdCardContent = "ML models will automatically detect & parse your number plate and determine the amount owing for your parking session.";



    return (
      <div class="container">
        <Title>Welcome to Autopark!</Title>
        <Subtitle>This prototype is designed to ingest an image of a vehicle assuming its numberplate is visible,
           and will detect the numberplate in the image and parse the number plate digits and letters. </Subtitle>
        <div class="homeDeck">
          <CardDeck>
            <Card 
            header={firstCardHeader}
            title={firstCardTitle}
            content={firstCardContent}
            />
            <Card 
            header={secondCardHeader}
            title={secondCardTitle}
            content={secondCardContent}
            />
            <Card 
            header={thirdCardHeader}
            title={thirdCardTitle}
            content={thirdCardContent}
            />
          </CardDeck>
        </div>
        <div class="getStarted">
          <Title>Get started!</Title>
          <div class="uploadBtn">
             <Button size="lg" class="uploadBtn" href="/uploader">Upload Image</Button>
          </div>
        </div> 
      </div>
    )
 }
}