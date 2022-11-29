var logged_in = false;

if (document.getElementById("false-false").innerHTML== "False"){
    console.log("FALSE ITS FALSE")
}
if (document.getElementById("false-false").innerHTML!= "False"){
    var name = document.getElementById("false-false").innerHTML
    sessionStorage.setItem("emails", `${name}`)
    console.log("11111111133342354")
    document.getElementById("true-false").innerHTML = sessionStorage.getItem("emails")
}



