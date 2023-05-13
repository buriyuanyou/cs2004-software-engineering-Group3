var score = 0;
// 获取所有选项按钮
var nextBtn_ban = document.getElementById("next-btn");
const optionButtons = document.querySelectorAll('.option button');

// 为每个选项按钮添加事件监听器
optionButtons.forEach(button => {
    button.addEventListener('click', () => {
        //做出选择后可以前往下一题
        nextBtn_ban.disabled = false;

        // 遍历所有选项按钮
        optionButtons.forEach(button => {
            //做出选择后无法再次选择
            button.disabled = true;
        });
        // 获取所选项对应题目的编号
        const selectedid = button.value;
        // 获取用户所选答案的值
        const selectedopt = button.innerHTML;

        // 将数据编码成 JSON 格式
        const data = {
            id: selectedid,
            answer: selectedopt
        };
        const jsonData = JSON.stringify(data);

        // 发送 AJAX 请求
        fetch('/answer_test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: jsonData
        })
            .then(response => response.json())
            .then(data => {
                // 处理返回的数据
                const isCorrect = data.result;
                const correctAnswer = data.answer;

                // 根据 isCorrect 显示提示信息
                if (isCorrect) {
                    score++;
                    button.style.backgroundColor = "rgba(9, 255, 0, 0.675)";
                } else {
                    button.style.backgroundColor = "rgba(255, 0, 0, 0.7)";
                    // 要等待 0.5 秒后执行的代码
                    setTimeout(function () {
                        // 遍历所有选项按钮
                        optionButtons.forEach(button => {
                            // 如果该按钮的innerHTML等于正确答案
                            if (button.innerHTML === correctAnswer) {
                                // 将其背景设为绿色
                                button.style.backgroundColor = "rgba(9, 255, 0, 0.675)";
                            }
                        });
                    }, 500);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
