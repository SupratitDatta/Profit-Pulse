import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCnA-fbWuIg3VTuuLZGLbRXaa7wRrrMmYs",
    authDomain: "profit-pulse-127.firebaseapp.com",
    projectId: "profit-pulse-127",
    storageBucket: "profit-pulse-127.appspot.com",
    messagingSenderId: "503643368622",
    appId: "1:503643368622:web:77411b596505b280a2d13f",
    measurementId: "G-M4F50PCDG7"
};

const app = initializeApp(firebaseConfig);

export const firebaseAuth = getAuth(app);