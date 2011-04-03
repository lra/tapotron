var count = 0;
var previous_count = 0;


var first_timestamp = 0;
var max_duration = 60000;

var cache = [];
var timer;

function sendResult() {
 $.get('/putScore/'+uid+'/'+count+'/', function(data) {
   if (data == 0) {
     alert('error');
   } else {
     alert('Score saved'); 
   }
 });
}



//preload the two states of the image
function preloadImages() {
    var cacheImage = document.createElement('img');
    cacheImage.src = '/cdn/button_up.png';
    cache.push(cacheImage);
    
    var cacheImage2 = document.createElement('img');
    cacheImage2.src = '/cdn/button_down.png';
    cache.push(cacheImage2);
}

// change the image
function changeImage() {
  document.getElementById('player').play();
  $('#button_image').attr('src',cache[count % 2].src);
}


// registers keyboard and mouse to listen to each press
function setUpListeners() {
  $('body').click(function(event) {
    incrementCounter(event);
  });

  $('body').keypress(function(event) {
    incrementCounter(event);
  });
}

// set the first timestamp : start of the game
function startTimer(event) {
  displayClicks();
  first_timestamp = event.timeStamp;
}

function displayClicks() {
  var current = count - previous_count;
  $('#graph-container').append('<div class="graph-points" style="height:'+(current*10+1)+'px">');
  previous_count = count;
  timer = setTimeout(displayClicks,100);
}


// increments the counter. If the counter was empty, start the timer.
// if not check that the current timer is below the max duration of the timer.
function incrementCounter(event) {
  if (count == 0 ) {
    startTimer(event);
    count = count + 1;
    changeImage();
  } else {

    if ( (event.timeStamp - first_timestamp) < max_duration) {
      count = count + 1;
      changeImage();
      $('#counter').text(count);
      $('#time').text((event.timeStamp - first_timestamp));
    } else {
      clearTimeout(timer);
      sendResult();
      count = 0; 
    } 
  }
}

$(document).ready(function(){
  preloadImages(['button_up.png','button_down.png']);
  changeImage();
  setUpListeners();
});



