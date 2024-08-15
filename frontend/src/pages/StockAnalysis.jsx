import React, { useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import Navbar from '../components/Navbar';
import '../css/stockanalysis.css';

function StockAnalysis() {
    const [file, setFile] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [chartData, setChartData] = useState([]);

    const handleFileUpload = (e) => {
        setFile(e.target.files[0]);
    };

    const analyzeStock = async (e) => {
        e.preventDefault();

        if (!file) {
            setAnalysisResult('Please upload a file before analyzing.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('/api/analyze-stock', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setAnalysisResult(response.data.result);
            setChartData(response.data.chartData);
        }
        catch (error) {
            console.error('Error analyzing stock:', error);
            setAnalysisResult('Error analyzing stock');
            setChartData([]);
        }
    };

    return (
        <>
            <Navbar />
            <div className="stock-analysis">
                <div className="content">
                    <h2>Stock Analysis</h2>
                    <form onSubmit={analyzeStock}>
                        <input type="file" accept=".csv" onChange={handleFileUpload} required />
                        <button class="button-86" type="submit">Analyze Stock</button>
                    </form>
                    {analysisResult && (
                        <div className="analysis-result">
                            <h3>Analysis Result:</h3>
                            <p>{analysisResult}</p>
                        </div>
                    )}
                    {chartData.length > 0 ? (
                        <div className="chart">
                            <h3>Seasonal Trend</h3>
                            <LineChart width={600} height={300} data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="sales" stroke="#8884d8" />
                            </LineChart>
                        </div>
                    ) : (
                        chartData.length === 0 && analysisResult && <p>No chart data available.</p>
                    )}
                </div>
            </div></>
    );
}

export default StockAnalysis;