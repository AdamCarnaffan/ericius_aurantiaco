import firebase from 'firebase'

// Your web app's Firebase configuration
let firebaseConfig = {
    apiKey: "AIzaSyDNq7q5reVP8daTySkuwoOGeeNfChmtrzo",
    authDomain: "honesty-matters-news.firebaseapp.com",
    databaseURL: "https://honesty-matters-news.firebaseio.com",
    projectId: "honesty-matters-news",
    storageBucket: "honesty-matters-news.appspot.com",
    messagingSenderId: "162246276993",
    appId: "1:162246276993:web:4dd64915b3a09b5442da80"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

export default firebase;