import React from 'react';
import '../css/about.css';

const AboutUs = () => {
    return (
        <div className="about-us" id="about">
            <header className="about-us-header">
                <h1>About Us</h1>
            </header>
            <div className="about-us-content">
                <div className="about-us-wrapper">
                    <div className="about-us-text">
                        <section className="mission">
                            <h2>Helping businesses succeed through the power of AI.</h2>
                            <p>We strive to create innovative solutions that make a positive impact on the world, one line of code at a time.</p>
                        </section>

                        <section className="values">
                            <h2>Our Values</h2>
                            <ul>
                                <li>Innovation</li>
                                <li>Integrity</li>
                                <li>Collaboration</li>
                                <li>Excellence</li>
                            </ul>
                        </section>
                    </div>
                    <div className="about-us-image">
                        <img src="https://www.vidyard.com/wp-content/themes/vidyard-website/img/pages/company/about-us/main-image.png.webp" alt="About Us" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AboutUs;
