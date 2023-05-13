
fetch('/post_question/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    }
})
    .then(response => response.json())
    .then(data => {
        // 解码返回的JSON数据
        const id = data.id;
        const question = data.question;
        const options = data.answer;
        const image_url = data.image_url;

        // 将数据呈现在web界面上
        document.getElementById('question-num').innerHTML = "Question 1:";
        document.getElementById("question").innerHTML = question;
        document.getElementById("testimg").src = image_url;

        for (let i = 1; i <= 4; i++) {
            const optionElem = document.getElementById("option" + i + "-btn");
            optionElem.value = id;
            // 设置选项的文本内容
            optionElem.innerHTML = `${options[i - 1]}`;
        }

    })
    .catch(error => {
        console.error('Error:', error);
    });

var questionnum = 2;
// 获取所有选项按钮
const optionButtons_clean = document.querySelectorAll('.option button');
var nextBtn = document.getElementById("next-btn");
//未作出选择前无法前往下一题
nextBtn.disabled = true;
nextBtn.addEventListener("click", function () {
    //未作出选择前无法前往下一题
    nextBtn.disabled = true;
    // 遍历所有选项按钮
    optionButtons_clean.forEach(button => {
        button.style.backgroundColor = "rgba(76, 0, 9, 0.65)";
        button.disabled = false;
    });

    if (questionnum < 10) {
        fetch('/post_question/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            }
        })
            .then(response => response.json())
            .then(data => {
                // 解码返回的JSON数据
                const id = data.id;
                const question = data.question;
                const options = data.answer;
                const image_url = data.image_url;

                // 将数据呈现在web界面上
                document.getElementById('question-num').innerHTML = "Question " + questionnum + ":";
                document.getElementById("question").innerHTML = question;
                document.getElementById("testimg").src = image_url;
                questionnum++;

                for (let i = 1; i <= 4; i++) {
                    const optionElem = document.getElementById("option" + i + "-btn");
                    optionElem.value = id;
                    // 设置选项的文本内容
                    optionElem.innerHTML = `${options[i - 1]}`;
                }

            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        //next按钮设置为不可见
        nextBtn.disabled = true;
        nextBtn.style.display = "none";
        fetch('/post_question/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            }
        })
            .then(response => response.json())
            .then(data => {
                // 解码返回的JSON数据
                const id = data.id;
                const question = data.question;
                const options = data.answer;
                const image_url = data.image_url;

                // 将数据呈现在web界面上
                document.getElementById('question-num').innerHTML = "Question " + questionnum + ":";
                document.getElementById("question").innerHTML = question;
                document.getElementById("testimg").src = image_url;

                for (let i = 1; i <= 4; i++) {
                    const optionElem = document.getElementById("option" + i + "-btn");
                    optionElem.value = id;
                    // 设置选项的文本内容
                    optionElem.innerHTML = `${options[i - 1]}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});

