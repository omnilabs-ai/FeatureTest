// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyADEMee2Q0OefwPIbP4igscwXdXnnchXio",
  authDomain: "omnilabs-43460.firebaseapp.com",
  projectId: "omnilabs-43460",
  storageBucket: "omnilabs-43460.firebasestorage.app",
  messagingSenderId: "1032196886867",
  appId: "1:1032196886867:web:48c7117d2ad1543871d1a6",
  measurementId: "G-CP9EZ3RM02"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();