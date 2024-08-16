import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import '../css/roicalculator.css';

function ROICalculator() {
    const [initialPrice, setInitialPrice] = useState('');
    const [rawSellPrice, setRawSellPrice] = useState('');
    const [discountedPrice, setDiscountedPrice] = useState('');
    const [profit, setProfit] = useState('');
    const [investment, setInvestment] = useState('');
    const [result, setResult] = useState('');

    const calculateROI = async (e) => {
        e.preventDefault();

        const data = {
            initialPrice: parseFloat(initialPrice),
            rawSellPrice: parseFloat(rawSellPrice),
            discountedPrice: parseFloat(discountedPrice),
            profit: parseFloat(profit),
            investment: parseFloat(investment)
        };

        if (Object.values(data).some(isNaN)) {
            setResult('Please enter valid numbers');
            return;
        }

        try {
            const response = await axios.post('http://localhost:5005/api/roi/predict', data);
            setResult(`Predicted ROI: ${response.data.roi.toFixed(2)}%`);
        }
        catch (error) {
            console.error('Error predicting ROI:', error);
            setResult('Error predicting ROI');
        }
    };

    return (
        <div className="roi-container">
            <Navbar />
            <div className="roi-calculator">
                <h2>ROI Calculator</h2>
                <form onSubmit={calculateROI}>
                    <input
                        type="number"
                        placeholder="Initial Price"
                        value={initialPrice}
                        onChange={(e) => setInitialPrice(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Raw Sell Price"
                        value={rawSellPrice}
                        onChange={(e) => setRawSellPrice(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Discounted Price"
                        value={discountedPrice}
                        onChange={(e) => setDiscountedPrice(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Profit"
                        value={profit}
                        onChange={(e) => setProfit(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Investment"
                        value={investment}
                        onChange={(e) => setInvestment(e.target.value)}
                        required />

                    <div className="lol">
                        <button className="button-86" type="submit">Predict</button>
                    </div>
                </form>
                {result && <p className="result">{result}</p>}
            </div>
        </div>
    );
}

export default ROICalculator;