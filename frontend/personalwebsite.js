
document.querySelectorAll(".floppy-all").forEach((link) =>{
  link.addEventListener("mouseover", () =>{
    console.log("mouse is over link");
      /*3px border */
      if (link.classList.contains("floppy-projects")) {
          document.querySelector("#dittoMac").src = "pngs/macintosh128khardhat.png"
      }
      else if (link.classList.contains("floppy-about")) {
          document.querySelector("#dittoMac").src = "pngs/macintosh128keyes.png"
      }
      else if (link.classList.contains("floppy-resume")) {
          document.querySelector("#dittoMac").src = "pngs/macintosh128kresume.png"
      }
  })
})

document.querySelectorAll(".floppy-all").forEach((link) =>{
  link.addEventListener("mouseout", () =>{
    console.log("mouse is over link");
    document.querySelector("#dittoMac").src = "pngs/macintosh128kditto.png"
  })
})

console.log("this is working");
/*
function mouseoverImage() {
    document.getElementById("dittoMac").src ="pngs/macintosh128kspotify.png"
}

function mouseoutImage() {
  document.getElementById("dittoMac").src ="pngs/macintosh128kditto.png"
}
*/
/*
random code i made to check if event listener could be added to smth else
window.onload=function(){
var item = document.getElementById("dittoMac");
  item.addEventListener("mouseover", func, false);
function func() {
  item.src="pngs/macintosh128kspotify.png"
  }
}
*/
