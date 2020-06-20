import React from 'react';
import axios from 'axios';
import {withRouter} from "react-router";

function UploaderComp(props) {
  const onSubmit = (event) => {
    event.preventDefault();
    postImage(event.target)
  };

  function postImage(form) {
    const url = 'http://localhost:5000/predict';

    var formData = new FormData(form);

    axios.post(url, formData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .then(response => {
        console.log(response);
        props.history.push('/summary', {data: response.data});
      })
      .catch(err => console.error(err));
  }

  return (
    <div className="container">
      <h3>Uploader</h3>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label htmlFor="num_plate">Please select an image to upload below:</label>
          <input type="file" className="form-control" name="num_plate" id="num_plate" aria-describedby="emailHelp" />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div >
  );
}

const Uploader = withRouter(UploaderComp);
export default Uploader;
