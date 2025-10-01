// preparing and cooking names
const registorform= document.getElementById("registorform");

registorform.addEventListener("submit",registerboy)


const username= document.getElementById("username");
const email= document.getElementById("email");
const passhash= document.getElementById("passhash");
const reg_result= document.getElementById("reg_result");



const regisbtn= document.getElementById("registerbtn");
const loginbtn= document.getElementById("signinbtn");

loginbtn.addEventListener("click",tologinpage)
function tologinpage(){
    window.location.href='/loginpage'
}

// registered succesfully

async function registerboy(e){
    e.preventDefault();

    const response= await fetch('https://holciye-video-platform.onrender.com/register',{
        method:"POST",
        headers:{"Content-type":"application/json"},
        body:JSON.stringify({username:username.value,email:email.value,passhash:passhash.value})
    });

    const data= await response.json();

    if(response.ok || data.Succes=="True"){

        reg_result.innerHTML=data.xanta;
        setTimeout(() => {
            window.location.href='/loginpage'
        }, 1000);
    } else{
        reg_result.innerHTML=data.xanta;
    }


}