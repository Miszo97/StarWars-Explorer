import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText } from '@mui/material';
import axios from 'axios';

const handleFetchCollection = async () => {
  try {
    const response = await axios.post('http://0.0.0.0:8000/api/generate');
    console.log('Data successfully fetched!');
  } catch (error) {
    console.error('Error fetching collection:', error.message);
  }
};

function CollectionList() {
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    fetch('http://0.0.0.0:8000/api/collections')
      .then(response => response.json())
      .then(data => {
        setCollections(data);
      });
  }, []);

  return (
    <div>
    <button onClick={handleFetchCollection}>Fetch collection</button>
    <List>
      {collections.map((collection, index) => (
        <ListItem key={index}>
          <ListItemText primary={<a href={`collections/${collection.id}`}>{collection.file_name}</a>} secondary={collection.created_at} />
        </ListItem>
      ))}
    </List>
    </div>
  );
}

export default CollectionList;
