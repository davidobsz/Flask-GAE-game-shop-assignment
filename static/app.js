import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-analytics.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAnhh49bESmre0PfzhiPfwucqDSNNpvdHk",
  authDomain: "storage-2cad3.firebaseapp.com",
  projectId: "storage-2cad3",
  storageBucket: "storage-2cad3.appspot.com",
  messagingSenderId: "427956143423",
  appId: "1:427956143423:web:f44e63513bbbcdabe57f8a",
  measurementId: "G-FRVC2X3NDD"
};
var logged_in = false
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

const submitButton = document.getElementById("submit");
const signupButton = document.getElementById("sign-up");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const main = document.getElementById("main");
const createacct = document.getElementById("create-acct")

const signupEmailIn = document.getElementById("email-signup");
const confirmSignupEmailIn = document.getElementById("confirm-email-signup");
const signupPasswordIn = document.getElementById("password-signup");
const confirmSignUpPasswordIn = document.getElementById("confirm-password-signup");
const createacctbtn = document.getElementById("create-acct-btn");

const returnBtn = document.getElementById("return-btn");

var email, password, signupEmail, signupPassword, confirmSignupEmail, confirmSignUpPassword;

createacctbtn.addEventListener("click", function() {
  var isVerified = true;

  signupEmail = signupEmailIn.value;
  confirmSignupEmail = confirmSignupEmailIn.value;
  if(signupEmail != confirmSignupEmail) {
      window.alert("Email fields do not match. Try again.")
      isVerified = false;
  }

  signupPassword = signupPasswordIn.value;
  confirmSignUpPassword = confirmSignUpPasswordIn.value;
  if(signupPassword != confirmSignUpPassword) {
      window.alert("Password fields do not match. Try again.")
      isVerified = false;
  }

  if(signupEmail == null || confirmSignupEmail == null || signupPassword == null || confirmSignUpPassword == null) {
    window.alert("Please fill out all required fields.");
    isVerified = false;
  }

  if(isVerified) {
    createUserWithEmailAndPassword(auth, signupEmail, signupPassword)
      .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      // ...
      window.alert("Success! Account created.");

    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      document.getElementById("allowed-or-not").innerHTML= "FALSE-LOGGED-IN-NOT"
      // ..
      //window.alert("Error occurred. Try again.");
    });
  }
});



submitButton.addEventListener("click", function() {
  email = emailInput.value;
  console.log(email);
  password = passwordInput.value;
  console.log(password);

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      logged_in = true
      window.alert("Success! Welcome back!");
      sessionStorage.setItem("logged-in-t-f", "TRUE-ALLOWED-LOGGED-IN")
      document.getElementById("allowed-or-not").innerHTML = sessionStorage.getItem("logged-in-t-f")
      sessionStorage.setItem("email", email)
      myfunction()
      location.reload()

      // ...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      sessionStorage.setItem("logged-in-t-f", "FALSE-NOALLOWED-LOGGED-OUT")
      document.getElementById("allowed-or-not").innerHTML = sessionStorage.getItem("logged-in-t-f")
      console.log("Error occurred. Try again.");
      window.alert("Error occurred. Try again.");
    });
});

signupButton.addEventListener("click", function() {
    main.style.display = "none";
    createacct.style.display = "block";
});

returnBtn.addEventListener("click", function() {
    main.style.display = "block";
    createacct.style.display = "none";
});
    function myfunction() {

        const firstname = email
        const lastname = "none"


        const dict_values = {firstname, lastname} //Pass the javascript variables to a dictionary.
        const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
        console.log(s); // Prints the variables to console window, which are in the JSON format
        $.ajax({
            url:"/logged-in",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s)});

}



if (sessionStorage.getItem('email') != null){
    loadLogggedInUser()
}

function  loadLogggedInUser(){
    document.getElementById("false-false").innerHTML = sessionStorage.getItem("email")
}


