import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './layouts/Layout';
import Home from './pages/Home';
import Gallery from './pages/Gallery';
import Design from './pages/Design';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/gallery" element={<Gallery />} />
          <Route path="/design" element={<Design />} />
          {/* <Route path="/pricing" element={<div style={{color: 'white', paddingTop: '100px', textAlign: 'center'}}>Pricing Page - Coming Soon!</div>} /> */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
