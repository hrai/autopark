import React from 'react';
import {withRouter} from "react-router";


function SummaryComp(props) {

  const data = props.location.state.data;

  return (
    <div class="container">
      {data['amount']}
    </div>
  );
}

const Summary = withRouter(SummaryComp);
export default Summary;
