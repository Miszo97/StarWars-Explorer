import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

function CsvTable() {
  const [csvData, setCsvData] = useState([]);

  useEffect(() => {
    fetch('http://0.0.0.0:8000/get_csv')
      .then(response => response.text())
      .then(data => {
        const rows = data.split('\n').map(row => row.split(','));
        setCsvData(rows);
      });
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            {csvData[0] && csvData[0].map((header, index) => (
              <TableCell key={index}>{header}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {csvData.slice(1).map((row, index) => (
            <TableRow key={index}>
              {row.map((cell, index) => (
                <TableCell key={index}>{cell}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default CsvTable;
