var status = 0; // 0:停止中 1:動作中
var time = 0;
var startBtn = document.getElementById("startBtn");
var timerLabel = document.getElementById('timerLabel');

// STARTボタン
function start() {
  // 動作中にする
  status = 1;
  // スタートボタンを押せないようにする
  startBtn.disabled = true;

  timer();
}

// STOPボタン
function stop() {
  // 停止中にする
  status = 0;
  // スタートボタンを押せるようにする
  startBtn.disabled = false;
}

// RESETボタン
function reset() {
  // 停止中にする
  status = 0;
  // タイムを0に戻す
  time = 0;
  // タイマーラベルをリセット
  timerLabel.innerHTML = '00:00';
  // スタートボタンを押せるようにする
  startBtn.disabled = false;
}

function timer() {
  // ステータスが動作中の場合のみ実行
  if (status == 1) {
    setTimeout(function () {
      time++;

      // 分・秒・ミリ秒を計算
      var min = Math.floor(time / 100 / 60);
      var sec = Math.floor(time / 100);
      var mSec = time % 100;

      if (min < 10) min = "0" + min;
      if (sec >= 60) sec = sec % 60;
      if (sec < 10) sec = "0" + sec;

      // タイマーラベルを更新
      timerLabel.innerHTML = min + ":" + sec;

      // 再びtimer()を呼び出す
      timer();
    }, 10);
  }
}

document.onkeydown = function (event) {
  if (event) {
    if (event.keyCode == 32 || event.which == 32) {
      if (status == 1) {
        stop();
      } else if (status == 0) {
        start();
      }
    }
  }
};

// テスト用
function changeColor(idname) {
  var obj = document.getElementById(idname);
  obj.style.color = '#ffffff';            //文字色を白にする
  obj.style.backgroundColor = '#ff0000';  //背景色を赤にする
}