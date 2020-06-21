import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
  th: {
    fontWeight: "bold"
  }
});

function createData(numPlate, parkedTime, amount, paid, date) {
  return {numPlate, parkedTime, amount, paid, date};
}

const rows = [
  createData('AWK477', '24m', 5.0, true, '20 March 2019'),
  createData('AWK477', '3hr 23m', 20.0, true, '20 May 2019'),
  createData('AWK477', '2hr 33m', 15.0, true, '30 June 2019'),
  createData('AWK477', '1hr', 10.0, true, '20 June 2019'),
];

export default function Visits() {
  const classes = useStyles();

  return (
    <div class="container">
      <h3>Visits</h3>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell className={classes.th}>Number Plate</TableCell>
              <TableCell className={classes.th} align="right">Parked Time</TableCell>
              <TableCell className={classes.th} align="right">Amount ($)</TableCell>
              <TableCell className={classes.th} align="right">Paid</TableCell>
              <TableCell className={classes.th} align="right">Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.name}>
                <TableCell component="th" scope="row">
                  {row.numPlate}
                </TableCell>
                <TableCell align="right">{row.parkedTime}</TableCell>
                <TableCell align="right">{row.amount}</TableCell>
                <TableCell align="right">{row.paid ? 'Yes' : 'No'}</TableCell>
                <TableCell align="right">{row.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
