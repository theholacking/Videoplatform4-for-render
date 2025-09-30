const logoutBtn = document.getElementById("logoutBtn");

document.addEventListener("DOMContentLoaded", function () {
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", function () {
        window.location.href = "/log_out";
    });
}



const to_dashb = document.getElementById("to_dashb");

to_dashb.addEventListener("click",to_dashbaord);


function to_dashbaord(){
    window.location.href="/dashboard";
}



});
const menuicon = document.querySelector(".menuicon");
const sidebar = document.querySelector(".sidebar");
const listcontainer = document.querySelector(".listcontainer");

menuicon.addEventListener("click",function shahwah() {
    sidebar.classList.toggle("smallsidebar");
    listcontainer.classList.toggle("smallcontainer")  ;
});

