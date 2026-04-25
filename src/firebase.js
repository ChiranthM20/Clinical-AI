// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCaZEUZ0AanH8CSIIyq_aZri1-aIkTFKwA",
  authDomain: "clinical-support.firebaseapp.com",
  projectId: "clinical-support",
  storageBucket: "clinical-support.firebasestorage.app",
  messagingSenderId: "727835719641",
  appId: "1:727835719641:web:1cbc89f1a5441460124bc8",
  measurementId: "G-9L9YBP05QH"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);