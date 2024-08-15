import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { firebaseAuth } from "../utils/firebaseConfig";
import { toast, ToastContainer } from 'react-toastify';
import '../css/login.css';

function Signup() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password.length < 8) {
            toast.error("Password must be at least 8 characters long");
            return;
        }

        if (password !== confirmPassword) {
            toast.error("Passwords Don't match");
            return;
        }

        try {
            await createUserWithEmailAndPassword(firebaseAuth, email, password);
            navigate('/');
        }
        catch (error) {
            toast.error("Error signing up, Please try again");
        }
    };

    const handleLoginRedirect = () => {
        navigate("/login");
    };

    const handleBackToHome = () => {
        navigate("/");
    };

    return (
        <>
            <button className="back-btn" onClick={handleBackToHome}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6 back-icon">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>
                <div>Back</div>
            </button>
            <div className="signup-container">
                <h2>Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Username:</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email:</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password:</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="confirmPassword">Confirm Password:</label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="submit-btn">Sign Up</button>
                </form>
                <div className="login-link">
                    <p>Already have an account? <span onClick={handleLoginRedirect} className="login-now">Login</span></p>
                </div>
            </div>
            <ToastContainer
                theme="dark"
                closeOnClick
                position="top-right"
                autoClose={5000}
            />
        </>
    );
}

export default Signup;