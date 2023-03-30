import './App.css';
import CsvTable from './CsvData';
import CollectionList from './Collections';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';



function App() {
  return (
    <Router>
      <div className="App">
        <h1>Star Wars</h1>
        <Routes>
          <Route path="/collections" element={<CollectionList />} />
          <Route path="/collections/:id" element={<CsvTable />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
