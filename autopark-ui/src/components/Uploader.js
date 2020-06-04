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
    <div class="container">
      <form onSubmit={onSubmit}>
        <div class="form-group">
          <label for="num_plate">Image</label>
          <input type="file" class="form-control" name="num_plate" id="num_plate" aria-describedby="emailHelp" />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div >
  );
}

const Uploader = withRouter(UploaderComp);
export default Uploader;
