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

function mix() {
  fetch('http://34.73.177.14/api/smooth-test')
    .then(response => response.text())
    .then(data => document.getElementById("audio-links").value = data)
}

function BufferLoader(context, urlList, callback) {
  this.context = context;
  this.urlList = urlList;
  this.onload = callback;
  this.bufferList = new Array();
  this.loadCount = 0;
}

BufferLoader.prototype.loadBuffer = function(url, index) {
  // Load buffer asynchronously
  var request = new XMLHttpRequest();
  request.open("GET", url, true);
  request.responseType = "arraybuffer";

  var loader = this;

  request.onload = function() {
    // Asynchronously decode the audio file data in request.response
    loader.context.decodeAudioData(
      request.response,
      function(buffer) {
        if (!buffer) {
          alert('error decoding file data: ' + url);
          return;
        }
        loader.bufferList[index] = buffer;
        if (++loader.loadCount == loader.urlList.length)
          loader.onload(loader.bufferList);
      },
      function(error) {
        console.error('decodeAudioData error', error);
      }
    );
  }

  request.onerror = function() {
    alert('BufferLoader: XHR error');
  }

  request.send();
}

BufferLoader.prototype.load = function() {
  for (var i = 0; i < this.urlList.length; ++i)
  this.loadBuffer(this.urlList[i], i);
}

var context;
var bufferLoader;
var VolumeSample = {
};

// Gain node needs to be mutated by volume control.
var gainNode1 = null;
var gainNode2 = null;

var muteCounter1 = 0;
var muteCounter2 = 0;


VolumeSample.init = function() {
  // Fix up prefixing
  window.AudioContext = window.AudioContext || window.webkitAudioContext;
  context = new AudioContext();

  bufferLoader = new BufferLoader(
    context,
    [
      "https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_133_5.mp3?alt=media",
      "https://storage.googleapis.com/download/storage/v1/b/dropdowns-stems/o/Smooth_100_11.mp3?alt=media",
    ],
    VolumeSample.finishedLoading
    );

  bufferLoader.load();
}

VolumeSample.finishedLoading = function(bufferList) {
	console.log("Done loading!")
  
  if (!context.createGain) {
    context.createGain = context.createGainNode;
  }
  gainNode1 = context.createGain();
  gainNode2 = context.createGain();
  
  // Create two sources and play them both together.
  var source1 = context.createBufferSource();
  var source2 = context.createBufferSource();
  
  source1.buffer = bufferList[0];
  source2.buffer = bufferList[1];
  
  source1.connect(gainNode1)
  source2.connect(gainNode2)
  
  gainNode1.connect(context.destination)
  gainNode2.connect(context.destination)
  
  source1.start(0);
  source2.start(0);
  
  this.source1 = source1
  this.source2 = source2
}

VolumeSample.toggleVolume1 = function(element) {
	console.log(muteCounter1);
	if (muteCounter1 % 2 === 0) {
		gainNode1.gain.value = 0;
	} else {
		gainNode1.gain.value = 1;
	}
	muteCounter1 += 1;
}

VolumeSample.toggleVolume2 = function(element) {
	console.log(muteCounter2);
	if (muteCounter2 % 2 === 0) {
		gainNode2.gain.value = 0;
	} else {
		gainNode2.gain.value = 1;
	}
	muteCounter2 += 1;
}
