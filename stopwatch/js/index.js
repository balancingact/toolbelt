var minute = 0;
var second = 0;
var millisecond = 0;
var timer = false;

function resetTimer(){
  minute = 0;
  second = 0;
  millisecond = 0;
  $("#minute").html(("00" + minute).slice(-3));
  $("#second").html(("0" + second).slice(-2));
  $("#millisecond").html(("0" + millisecond).slice(-1));
}

function runWatch(){
  millisecond += 1;
  if((millisecond % 10) == 0){
    millisecond = 0;
    second += 1;
  }
  if((second % 60) == 0 && millisecond == 0){
    second = 0;
    minute += 1;
  }
  $("#minute").html(("00" + minute).slice(-3));
  $("#second").html(("0" + second).slice(-2));
  $("#millisecond").html(("0" + millisecond).slice(-1));

  timer = setInterval(function(){
    millisecond += 1;
    if((millisecond % 10) == 0){
      millisecond = 0;
      second += 1;
    }
    if((second % 60) == 0 && millisecond == 0){
      second = 0;
      minute += 1;
    }
    $("#minute").html(("00" + minute).slice(-3));
    $("#second").html(("0" + second).slice(-2));
    $("#millisecond").html(("0" + millisecond).slice(-1));
  }, 100);
}

function saveScore(){
  var player = prompt("Please enter your name", "Ernő Rubik");
  if (player) {
    var score = (minute * 60) + second + (0.1 * millisecond);

    $.getJSON("http://192.168.73.17:23456/saveScore?player=" + player + "&score=" + score, function(result){
        $('#high-scores').empty();
        highScores();
    });
  }
}

function scoreboard(){
  $.getJSON("http://192.168.73.17:23456/scoreboard", function(result){
      scoreboard = result['scores'].split(',');
      $.each(scoreboard, function (index, value) {
        $("#high-scores").append('<li>' + value + '</li>');
      });
  });
}

function highScores(){
  $.getJSON("http://192.168.73.17:23456/highscores", function(result){
      scoreboard = result['scores'].split(',');
      $.each(scoreboard, function (index, value) {
        $("#high-scores").append('<li>' + value + '</li>');
      });
  });

}
