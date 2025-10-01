const uploadbtn = document.getElementById("uploadbtn");

const choosefile = document.getElementById("choosefile");
const videohd = document.getElementsByClassName("videohd");


choosefile.addEventListener("change", () => {
  
  const file = choosefile.files[0];
  if (file) {
    
    const video_url = URL.createObjectURL(file);
    console.log(video_url);
    thepreviewvid.src = video_url;
    thepreviewvid.load();
    thepreviewvid.play();
    videohd.style.background

    thepreviewvid.addEventListener("loadedmetadata",()=>{

      console.log(thepreviewvid.duration)
    });
 }
});

uploadbtn.addEventListener("click", cloudfare);


async function cloudfare(e) {
  e.preventDefault();

  const titlein = document.getElementById("title");
  const title = document.getElementById("title").value;
  const result = document.getElementById("checktext");
  const choosefile = document.getElementById("choosefile");
  const file = choosefile.files[0];
  const progressbar = document.getElementById("progressbar");


  if (!file) return result.innerHTML = "<h4>Select a video! qashinow 😂🤣</h4>";
  if (title.trim()=="") return result.innerHTML = "<h4>qoraalka neh! qashinow 😂🤣</h4>"; +  titlein.focus();;

    
    

  const formData = new FormData();
  formData.append("title", title);
  formData.append("video", file);

 try{ 
  const response = await fetch("https://holciye-video-platform.onrender.com/upload", {
    method: "POST",
    body: formData
  });

  if (response.ok) {
    const data = await response.json();  
    console.log(data.url);
    result.innerHTML = data.xanaan;
    progressbar.style.width="100%";
    setInterval(() => {
      window.location.href="/videos"
    }, 3000);


  } else {
    const text = await response.text();
    result.innerHTML = `yaahuu`;

  }
}
   catch(err){
    console.error("Network error:", err);
    result.innerHTML = "🚨 Network/Server error — check Flask logs.";
  }

}