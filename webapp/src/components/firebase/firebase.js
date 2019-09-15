import app from 'firebase/app';
import 'firebase/database';

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDNq7q5reVP8daTySkuwoOGeeNfChmtrzo",
    authDomain: "honesty-matters-news.firebaseapp.com",
    databaseURL: "https://honesty-matters-news.firebaseio.com",
    projectId: "honesty-matters-news",
    storageBucket: "honesty-matters-news.appspot.com",
    messagingSenderId: "162246276993",
    appId: "1:162246276993:web:4dd64915b3a09b5442da80"
};

class Firebase {
  constructor() {
    app.initializeApp(firebaseConfig);
    this.db = app.database();
  }
}
export default Firebase;