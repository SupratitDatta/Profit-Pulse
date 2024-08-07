import React from 'react';
import "../css/hero.css";

function Hero() {
    return (
        <div>
            <section class="hero">
                <h1>Your One-Stop Solution for Retail Stock Growth!</h1>
                <div class="btn-group">
                    <button class="btn-outline-dark btn-hover-color">Return On<span class="material-symbols-outlined">
                        Investment
                    </span></button>
                    <button class="btn-outline-dark btn-hover-color">Stock<span class="material-symbols-outlined">
                        Analysis
                    </span></button>
                    <button class="btn-outline-dark btn-hover-color">Business<span class="material-symbols-outlined">
                        Strategies
                    </span></button>
                </div>
            </section>
        </div>
    )
}

export default Hero;