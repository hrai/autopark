import React from 'react';
import {withRouter} from "react-router";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles({
  table: {
    minWidth: 150,
    // width: 450,
  },
  th: {
    fontWeight: "bold",
  },
  img: {
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    width: "25%",
    padding: "20px",
  },
  plate: {
    fontWeight: "bold",
    textAlign: "center",
  }
});

function SummaryComp(props) {
  const classes = useStyles();
  const data = props.location.state.data;

  const imageData = data.image_b64;
  const imageContent = `data:image/png;base64,${imageData}`;

  return (
    <div class="container">
      <h3>Summary</h3>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            <TableRow key="1">
              <TableCell component="th" scope="row" className={classes.th}>
                Start Time
                </TableCell>
              <TableCell align="right">{data.startTime}</TableCell>
            </TableRow>
            <TableRow key="2" >
              <TableCell component="th" scope="row" className={classes.th}>
                Finish Time
                </TableCell>
              <TableCell align="right">{data.finishTime}</TableCell>
            </TableRow>
            <TableRow key="3">
              <TableCell component="th" scope="row" className={classes.th}>
                Total Time
              </TableCell>
              <TableCell align="right">{data.totalTime}</TableCell>
            </TableRow>
            <TableRow key="4">
              <TableCell component="th" scope="row" className={classes.th}>
                Amount
              </TableCell>
              <TableCell align="right">{data.amount}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer >
      <div>
        <img className={classes.img} src={imageContent} alt="number plate" />
        <p className={classes.plate}>Number plate: {data.numberPlate}</p>
      </div>
    </div >
  );
}

const Summary = withRouter(SummaryComp);
export default Summary;
