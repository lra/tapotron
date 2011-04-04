var count = 0;
var previous_count = 0;


var first_timestamp = 0;
var max_duration = 60000;

var cache = [];
var timer;
var current_time = 0;

var no_time;
var no_button_displayed = false;


function sendResult() {
 $.get('/putScore/'+uid+'/'+count+'/', function(data) {
   if (data == 0) {
     alert('Not your best score');
   } else {
     $('#best-score').text(count);
   }
  count = 0;
  previous_count = 0;
 });
}

function getBestScore() {
 $.get('/getScore/'+uid+'/',function(data) {
    var score = data.split(':');
    $('#best-score').text(score[1]);
  }
)
}

//preload the two states of the image
function preloadImages() {
    var cacheImage = document.createElement('img');
    cacheImage.src = '/cdn/button_up.png';
    cache.push(cacheImage);
    
    var cacheImage2 = document.createElement('img');
    cacheImage2.src = '/cdn/button_down.png';
    cache.push(cacheImage2);


    var cacheImage3 = document.createElement('img');
    cacheImage3.src = '/cdn/no.png';
    cache.push(cacheImage3);
}

// change the image
function changeImage() {
  document.getElementById('player').play();
  $('#button').attr('src',cache[count % 2].src);
}


// registers keyboard and mouse to listen to each press
function setUpListeners() {
  $('body').click(
    incrementCounter
  );

  $('body').keypress(
    incrementCounter
  );
}

function removeListeners() {
  $('body').unbind('click',incrementCounter);
  $('body').unbind('keypress',incrementCounter);

}

function displayNoButton() {
  if (no_button_displayed) {
    changeImage();
    no_button_displayed = false;
  } else {
    no_button_displayed = true;
    $('#button').attr('src',cache[2].src);
    setTimeout(displayNoButton,1000);
  }
}


// set the first timestamp : start of the game
function startTimer(event) {
  displayClicks();
  first_timestamp = event.timeStamp;
}

function displayClicks() {
  var current = count - previous_count;
  $('#graph-container').append('<div class="graph-points" style="height:'+(current + 1)+'px">');
  previous_count = count;
  timer = setTimeout(displayClicks,1000);
  current_time++;  
  if (current_time == no_time) {
    displayNoButton();
  }
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
      if (no_button_displayed) {
        count = Math.max(1,count - 100);
      } else {
       count = count + 1;
       changeImage();
      }
      $('#counter').text(count);
      $('#time').text((event.timeStamp - first_timestamp));
    } else {
      clearTimeout(timer);
      sendResult();
      stopGame();
    } 
  }
}

function stopGame() {
  $('#start-button').show();
  $('#button').hide();
  removeListeners();
}

function startNewGame() {
  $('#start-button').hide();
  $('#button').fadeIn('slow', function() {});

  $('#graph-container').empty();
  changeImage();
  setUpListeners(); 
  $('#counter').text(count);
  $('#time').text('0');
  no_time = Math.floor((Math.random()*(max_duration - 5000))/1000 + 5);

}

$(document).ready(function(){
  preloadImages(['button_up.png','button_down.png']);
  $('#start-button').click(function(){ startNewGame(); });
  getBestScore();
});



