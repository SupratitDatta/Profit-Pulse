import React from 'react'
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import AboutUs from "../components/AboutUs";

function Home() {
    return (
        <div>
            <Navbar />
            <Hero />
            <AboutUs />
        </div>
    )
}

export default Home;