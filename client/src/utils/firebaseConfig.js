// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
import { GoogleAuthProvider, getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDcf9wjGwxrl-Tfix3PK2SXeXn-nM_tn7c",
  authDomain: "delta-hacks-acd6d.firebaseapp.com",
  projectId: "delta-hacks-acd6d",
  storageBucket: "delta-hacks-acd6d.appspot.com",
  messagingSenderId: "278318449905",
  appId: "1:278318449905:web:761b331684b7835dec9550",
  measurementId: "G-5JGWN5J999"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
// const analytics = getAnalytics(app); 
const googleAuthProvider = new GoogleAuthProvider();
const db = getFirestore(app);

export { auth, googleAuthProvider, db };
