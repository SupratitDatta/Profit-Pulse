import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import '../css/ropcalculator.css';

function ROPCalculator() {
    const [quantity, setQuantity] = useState('');
    const [demandRate, setDemandRate] = useState('');
    const [daysReqToReceiveOrder, setDaysReqToReceiveOrder] = useState('');
    const [safetyStock, setSafetyStock] = useState('');
    const [result, setResult] = useState(null);

    const calculateROP = async (e) => {
        e.preventDefault();

        const data = {
            quantity: parseFloat(quantity),
            demand_rate: parseFloat(demandRate),
            days_req_to_receive_order: parseFloat(daysReqToReceiveOrder),
            safety_stock: parseFloat(safetyStock),
        };

        if (Object.values(data).some(isNaN)) {
            setResult({ error: 'Please enter valid numbers' });
            return;
        }
        try {
            const response = await axios.post('http://localhost:5000/api/rop/predict', data);
            setResult(`Predicted ROP: ${response.data.rop.toFixed(0)}`);
        }
        catch (error) {
            console.error('Error predicting ROP:', error);
            setResult({ error: 'Error predicting ROP' });
        }
    };

    return (
        <div className="rop-container">
            <Navbar />
            <div className="rop-calculator">
                <h2>ROP Calculator</h2>
                <form onSubmit={calculateROP}>
                    <input
                        type="number"
                        placeholder="Quantity"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Demand Rate"
                        value={demandRate}
                        onChange={(e) => setDemandRate(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Days Required to Receive Order"
                        value={daysReqToReceiveOrder}
                        onChange={(e) => setDaysReqToReceiveOrder(e.target.value)}
                        required />

                    <input
                        type="number"
                        placeholder="Safety Stock"
                        value={safetyStock}
                        onChange={(e) => setSafetyStock(e.target.value)}
                        required />

                    <div className="lol">
                        <button className="button-86" type="submit">Calculate ROP</button>
                    </div>
                </form>
                {result && result.error && <p className="result error">{result.error}</p>}
                {result && !result.error && (
                    <div className="result">
                        <p>{result}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ROPCalculator;