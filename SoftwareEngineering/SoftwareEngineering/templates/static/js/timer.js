
var endBtn = document.getElementById("end-btn");
endBtn.addEventListener("click", function () {
    var confirmEnd = confirm("Are you sure to end the test? Click OK to end the timer.");
    if (confirmEnd) {
        clearInterval(timerInterval);//结束计时
        var currentTime = new Date().getTime();
        var elapsedTime = currentTime - startTime;
        var minutes = Math.floor(elapsedTime / (1000 * 60));
        var seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
        var formattedTime = ("0" + minutes).slice(-2) + ":" + ("0" + seconds).slice(-2);
        timerElement.innerText = formattedTime;

        var message = "You have completed the test in " + formattedTime + ". SCORE :" + score + ".";
        alert(message); // 弹出提示框

        // 将答题时间和分数存储在 sessionStorage 中
        sessionStorage.setItem("formattedTime", formattedTime);
        sessionStorage.setItem("score", score);

        window.location.href = "answerrecord.html"; // 跳转
    }
});

var timerElement = document.getElementById("timer");
var startTime = new Date().getTime();

function updateTimer() {
    var currentTime = new Date().getTime();
    var elapsedTime = currentTime - startTime;
    var minutes = Math.floor(elapsedTime / (1000 * 60));
    var seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
    var formattedTime = ("0" + minutes).slice(-2) + ":" + ("0" + seconds).slice(-2);
    timerElement.innerText = formattedTime;
}

var timerInterval = setInterval(updateTimer, 1000);