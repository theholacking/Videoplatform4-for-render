// for index.html the sign up form in js
const form = document.getElementById("loginform");
form.addEventListener("submit", signin);

const username= document.getElementById("username");
const passhash = document.getElementById("passhash");
const result = document.getElementById("result");

async function signin(e) {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:5050/login",
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({username:username.value, passhash:passhash.value})
        });
    const data = await response.json();
    if (response.ok || data.succes=='True') {
        result.innerHTML = data.xanta;
        
        setTimeout(() => {
           window.location.href = '/videos'; 
        }, 3000);
        
    }
    else {
        result.innerHTML = "meesha iska soo gal ma ahan";
    }
};
// for returning to sign up page
const signupbtn = document.getElementById("signupbtn");
try {
    
signupbtn.addEventListener("click",to_register);


function to_register(){
    window.location.href="/log_out";
}
} catch (err) {
    console.error(err);
    
}
if (prev===false){
 prev===true
}
else{
    prev===false
}