import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import '../css/roicalculator.css';

function ROICalculator() {
    const [productPrice, setProductPrice] = useState('');
    const [marketingCost, setMarketingCost] = useState('');
    const [income, setIncome] = useState('');
    const [result, setResult] = useState('');

    const calculateROI = async (e) => {
        e.preventDefault();

        const price = parseFloat(productPrice);
        const cost = parseFloat(marketingCost);
        const revenue = parseFloat(income);

        if (isNaN(price) || isNaN(cost) || isNaN(revenue)) {
            setResult('Please enter valid numbers');
            return;
        }

        try {
            const roi = ((revenue - (price + cost)) / (price + cost)) * 100;
            setResult(`Your ROI is ${roi.toFixed(2)}%`);

            await axios.post('/api/calculate-roi', {
                productPrice: price,
                marketingCost: cost,
                income: revenue,
                roi
            });
        } 
        catch (error) {
            console.error('Error calculating ROI:', error);
            setResult('Error calculating ROI');
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
                        placeholder="Total Product Price"
                        value={productPrice}
                        onChange={(e) => setProductPrice(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Marketing Cost"
                        value={marketingCost}
                        onChange={(e) => setMarketingCost(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Income"
                        value={income}
                        onChange={(e) => setIncome(e.target.value)}
                        required />
                    <div className="lol">
                        <button class="button-86" type="submit">Calculate ROI</button>
                    </div>   </form>
                {result && <p className="result">{result}</p>}
            </div>
        </div>
    );
}

export default ROICalculator;