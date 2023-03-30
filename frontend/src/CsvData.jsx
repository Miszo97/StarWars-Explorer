import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Papa from 'papaparse';
import { Routes, Route, useParams } from 'react-router-dom';


function CsvTable(props) {
  const [csvData, setCsvData] = useState([]);
  const { id } = useParams()

  useEffect(() => {
    fetch(`http://0.0.0.0:8000/api/collections/${id}`)
      .then(response => response.text())
      .then(data => {
        const { data: rows } = Papa.parse(data, { header: true });
        setCsvData(rows);
      });
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            {csvData[0] && Object.keys(csvData[0]).map((header, index) => (
              <TableCell key={index}>{header}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {csvData.map((row, index) => (
            <TableRow key={index}>
              {Object.values(row).map((cell, index) => (
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
