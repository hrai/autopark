import React from 'react';
import { useForm } from "react-hook-form";


export default function Uploader() {
  // const {handleSubmit,register,errors}=useForm();
  const {handleSubmit}=useForm();
  const onSubmit=values=>console.log(values);

  return (
    <form onSubmit={ handleSubmit(onSubmit) }>
      <div class="form-group">
          <label for="uploader">Image</label>
          <input type="file" class="form-control" id="uploader" aria-describedby="emailHelp"/>
      </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  );
}
