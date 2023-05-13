function updateTable() {
    // 获取答题时间和分数
    var formattedTime = sessionStorage.getItem("formattedTime");
    var score = sessionStorage.getItem("score");

    // 创建新的表格行
    var newRow = document.createElement("tr");
    var newDate = new Date().toISOString().slice(0, 10); // 新行的日期为当前日期
    var newTimeSpent = formattedTime; // 新行的答题时间为格式化后的时间
    var newScore = score; // 计算新行的得分

    // 更新新行的数据
    newRow.innerHTML = "<td>" + 1 + "</td>" +
        "<td>" + newDate + "</td>" +
        "<td>" + newTimeSpent + "</td>" +
        "<td>" + newScore + "</td>";

    // 将新行插入到表格中
    var tableBody = document.querySelector("tbody");
    tableBody.insertBefore(newRow, tableBody.firstChild);

    // 将修改后的表格 HTML 代码保存至 localStorage 中
    var tableHtml = document.querySelector("table").outerHTML;
    localStorage.setItem("tableHtml", tableHtml);

    // 更新其余行的编号
    var rows = document.querySelectorAll("tbody tr");
    for (var i = 1; i < rows.length - 1; i++) {
        rows[i].querySelector("td:first-child").textContent = i + 1;
    }

    // 清空sessionStorage
    sessionStorage.removeItem("formattedTime");
    sessionStorage.removeItem("score");
}

function informationstatistic() {
    // 获取表格中的所有记录行
    var rows = document.querySelectorAll("tbody tr");
    for (var i = 1; i < rows.length - 1; i++) {
        rows[i].querySelector("td:first-child").textContent = i + 1;
    }

    // 统计记录数、总用时和总分数
    var rowCount = rows.length - 1;
    var totalTime = 0;
    var totalScore = 0;
    for (var i = 0; i < rowCount; i++) {
        var row = rows[i];
        var timeSpent = row.querySelector("td:nth-child(3)").textContent;
        var score = parseInt(row.querySelector("td:nth-child(4)").textContent);
        totalTime += timeToSeconds(timeSpent);
        totalScore += score;
    }

    // 计算平均用时和平均分数
    var avgTime = Math.round(totalTime / rowCount); // 取整数
    var avgScore = (totalScore / rowCount).toFixed(2); // 保留两位小数

    var rowCountdiv = document.getElementById("numoftest");
    var avgScorediv = document.getElementById("avgscore");
    var avgTimediv = document.getElementById("avgtime");

    rowCountdiv.innerHTML = "Number of tests : " + rowCount;
    avgScorediv.innerHTML = "Average score:" + avgScore;
    avgTimediv.innerHTML = "Average time:" + secondsToTime(avgTime);


    // 将结果输出到控制台
    console.log("Number of records: " + rowCount);
    console.log("Average time spent: " + secondsToTime(avgTime));
    console.log("Average score: " + avgScore);
}

// 使用window.onload方法，在页面加载完成后自动调用updateTable()函数
window.onload = function () {

    // 从 localStorage 中取出表格 HTML 代码，并设置为表格的 innerHTML 属性
    var tableHtml = localStorage.getItem("tableHtml");
    if (tableHtml) {
        document.querySelector("table").innerHTML = tableHtml;
    }

    // 获取答题时间和分数
    var formattedTime = sessionStorage.getItem("formattedTime");
    var score = sessionStorage.getItem("score");

    if (score != null && formattedTime != null) {
        updateTable();
    }
    informationstatistic();
}

// 将时间字符串转换为秒数的辅助函数
function timeToSeconds(timeStr) {
    var parts = timeStr.split(":");
    var minutes = parseInt(parts[0]);
    var seconds = parseInt(parts[1]);
    return minutes * 60 + seconds;
}

// 将秒数转换为时间字符串的辅助函数
function secondsToTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    var seconds = seconds % 60;
    return pad(minutes, 2) + ":" + pad(seconds, 2);
}

// 在数字前补零的辅助函数
function pad(num, size) {
    var s = "000000000" + num;
    return s.slice(-size);
}