/*

document.querySelectorAll(".floppy-all").forEach((link) =>{
  link.addEventListener("mouseover", () =>{
    console.log("mouse is over link");
      /*3px border */
/*
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

function mouseoverImage() {
    document.getElementById("dittoMac").src ="pngs/macintosh128kspotify.png"
}

function mouseoutImage() {
  document.getElementById("dittoMac").src ="pngs/macintosh128kditto.png"
}


random code i made to check if event listener could be added to smth else
window.onload=function(){
var item = document.getElementById("dittoMac");
  item.addEventListener("mouseover", func, false);
function func() {
  item.src="pngs/macintosh128kspotify.png"
  }
}
*/

//document.getElementById("two-songs")

function toggleSearchRow() {
  x = document.getElementById("search-row-2");
  y = document.getElementById("mood-row");
  if (x.style.display === "none") {
    x.style.display = "block"
    y.style.display = "none"
  } else {
    x.style.display = "none"
    y.style.display = "block"
  }
}

function toggleVocal1() {
  fetch('http://34.73.177.14/api/smooth-test').then(x => {
    // x here is a list of links separated by commas
    console.log(x)
  })
}