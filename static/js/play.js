document.addEventListener("DOMContentLoaded",function (){

// qeebta furitaanka ee comment section ka kkkkkkkkkkkkk
const commentTriggers = document.getElementById("commentsnum");
const commentSection = document.querySelector(".addcommentsmugdi");

commentTriggers.addEventListener("click",  function () {
        commentSection.classList.toggle("addcomments");  
    });


   //meesha lagu darayo commentiga  shahwah
   
   const addcommentbtn = document.getElementById("addcomment");
   const c_input = document.getElementById("c_input");
   

   addcommentbtn.addEventListener("click",siidaa);

   async function siidaa(e){
    e.preventDefault();
    console.log("yay uts clicked");
    console.log(video_id);

    const comment = c_input.value;

    const response = await fetch(`http://127.0.0.1:5050/videos/${video_id}/addcomment`,{

        method : "POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({comment})
   })

   const data = await response.json();
   if (response.ok || data.Succes =="xaaraan"){
   
        const commentTriggers = document.getElementById("commentsnum");
        const commentTriggerstext =parseInt( commentTriggers.textContent) || 0;

        commentTriggers.textContent= (commentTriggerstext+1) + " comments";

         c_input.value = "";

        alert(`comment posted bro ${data.qaanjeerta}`);

         
    }
    else{
        alert(`comment posted bro ${data.qaanjeerta}`);
    }




   };

 // shahwah da like ta iyo share ta
 const likebtn = document.getElementById("likebtn");
 const likenum = document.getElementById("likenum");

 likebtn.addEventListener("click",suulka);

  async function suulka(e) {
    e.preventDefault();
    
   const like_response = await fetch(`http://127.0.0.1:5050/videos/${video_id}/like_blue`,{
        method:"POST",
        headers:{"Content-Type":"application/json"}

    })
    const like_data = await like_response.json();
    if(like_response.ok || like_data.Succes == "True"){
        alert(`mhmm ${like_data.message}`)
        
        const likenumtext =parseInt( likenum.textContent) || 0;

        likenum.textContent= (likenumtext+1) + " likes";
        likebtn.style.backgrounColor = "blue"; 
    }else{
        alert(`mhmm ${like_data.message}`)
        likebtn.style.color = ""; 
    }


  }

});







