import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';


export default function Uploader() {
  // const {handleSubmit,register,errors}=useForm();
  const {handleSubmit}=useForm();

  /*
  postImage = (imageData) => {
    const url='http://localhost:5000/predict';
    axios.post(url, imageData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
      }
    });
  }
  */

  const onSubmit = values => postImage(values);

  function postImage(imageData) {
    const url='http://localhost:5000/predict';

    var bodyFormData=new FormData();
    bodyFormData.set('filename', 'TestFile');
    bodyFormData.append('image', imageData);

    axios.post(url, bodyFormData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'multipart/form-data',
      }
    })
    .then(resp=> console.log(resp))
    .catch(err=>console.error(err));
  }
  return (
    <div class="container">
      <form onSubmit={ handleSubmit(onSubmit) }>
        <div class="form-group">
            <label for="uploader">Image</label>
            <input type="file" class="form-control" id="uploader" aria-describedby="emailHelp"/>
        </div>
          <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  );
}
