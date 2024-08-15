import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ROICalculator from './pages/ROICalculator';
import StockAnalysis from './pages/StockAnalysis';
import BusinessStrategies from './pages/BusinessStrategies';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/roi-calculator" element={<ROICalculator />} />
                <Route path="/stock-analysis" element={<StockAnalysis />} />
                <Route path="/business-strategies" element={<BusinessStrategies />} />
                <Route path="/login" element={<Login/>} />
                <Route path="/signup" element={<Signup/>} />
            </Routes>
        </Router>
    );
}

export default App;