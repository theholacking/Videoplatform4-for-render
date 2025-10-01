
const uploadbtn = document.getElementById("uploadbtn");

uploadbtn.addEventListener("click",uploadpage);


function uploadpage(){
    window.location.href="/upload_page"
};

// qeebta furitaanka ee comment section ka kkkkkkkkkkkkk
const commentTriggers = document.querySelectorAll(".commentsnum");


commentTriggers.forEach(trigger => {
    trigger.addEventListener("click",  function () {
        // weyneenta comment section
        const videoContainer = trigger.closest(".videolists"); // get parent video section
        const commentSection = videoContainer.querySelector(".addcommentsmugdi");
        commentSection.classList.toggle("addcomments");  

    });
});

// qeebta kudarista comment cusub ee comment section ka kkkkkkkkkkkkk
// const addcommentbtn = document.querySelectorAll(".addcomment");
// addcommentbtn.forEach(btn => {
//     btn.addEventListener("click", async function (e){
//         e.preventDefault;
//         const response=await fetch("https://holciye-video-platform.onrender.com/videos")
        
       
//     })
// });


