from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
import json
import random
from django.views.decorators.csrf import csrf_exempt

# 使用一个列表来存储已经抛出的问题的下标
used_numbers = []

# 抛出问题
@csrf_exempt
def post_question(request):
    global used_numbers
    f = open('templates\static\question.json', encoding='utf-8')
    data = json.load(f)

    # 问题库被刷完，抛出一个消息提示(测试暂定，需更改,应返回一个提示响应)
    if len(data) == len(used_numbers):
        print("所有问题已经答完")
        used_numbers = []
        # return JsonResponse({"question": "所有问题已经答完！"})

    while True:
        # 随机数范围 0 - (len(data) - 1)
        number = random.randint(0, len(data) - 1)
        if number not in used_numbers:
            used_numbers.append(number)
            break
    # 答案列表，包括正确答案和错误答案
    answer_list = [data[number]["Fanswer1"], data[number]["Fanswer2"],
                   data[number]["Fanswer3"], data[number]["answer"]]
    # 随机排列
    random.shuffle(answer_list)

    return JsonResponse({"id": data[number]['id'],
                         "question": data[number]['question'],
                         "answer": answer_list,
                         "image_url": data[number]['image_url']})
# 验证答案
@csrf_exempt
def answer_test(request):
    if request.method == 'POST':
        json_str = request.body.decode()
        datas = json.loads(json_str)
        user_id = datas['id']
        user_answer = datas['answer']

        f = open('templates\static\question.json', encoding='utf-8')
        data = json.load(f)

        # 比对结果
        result = False
        # 正确答案
        answer = ''

        for number in range(len(data)):
            if data[number]['id'] == user_id and data[number]['answer'] == user_answer:
                result = True
                answer = data[number]['answer']
            if data[number]['id'] == user_id and data[number]['answer'] != user_answer:
                result = False
                answer = data[number]['answer']

        response_data = {'id':user_id,'result': result, 'answer': answer,'user_answer':user_answer}
        print(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'result': False})


def index(request):
    return render(request, 'index.html')

def ask(request):
    return render(request, 'ask.html')

def answerrecord(request):
    return render(request, 'answerrecord.html')

def answertest(request):
    return render(request, 'answertest.html')