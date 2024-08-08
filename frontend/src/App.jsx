import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ROICalculator from './pages/ROICalculator';
import StockAnalysis from './pages/StockAnalysis';
import Business from './pages/Business';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/roi-calculator" element={<ROICalculator />} />
                <Route path="/stock-analysis" element={<StockAnalysis />} />
                <Route path="/business-strategies" element={<Business />} />
            </Routes>
        </Router>
    );
}

export default App;