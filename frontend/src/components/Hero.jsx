import React from 'react';
import { Link } from 'react-router-dom';
import "../css/hero.css";

function Hero() {
    return (
        <div>
            <section className="hero">
                <h1>Your One-Stop Solution for Retail Stock Growth!</h1>
                <div className="btn-group">
                    <Link to="/roi-calculator">
                        <button className="btn-outline-dark btn-hover-color">Return On<span className="material-symbols-outlined">
                            Investment
                        </span></button>
                    </Link>
                    <Link to="/stock-analysis">
                        <button className="btn-outline-dark btn-hover-color">Stock<span className="material-symbols-outlined">
                            Analysis
                        </span></button>
                    </Link>
                    <Link to="/business-strategies">
                        <button className="btn-outline-dark btn-hover-color">Business<span className="material-symbols-outlined">
                            Strategies
                        </span></button>
                    </Link>
                </div>
            </section>
        </div>
    );
}

export default Hero;