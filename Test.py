from flask import Flask, render_template, request
import openai
import time

# Replace YOUR_API_KEY with your actual API key
prompt = ""
openai.api_key = "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"

# Set up the prompt and model parameters
model_engine = "text-davinci-002"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form['data']
    processed_data = process_data(data)
    return render_template('result.html', data=processed_data)

def process_data(data):
    # 在这里编写处理数据的代码
    prompt = data
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1000
    )
    text = response.choices[0].text.strip()
    return text

if __name__ == '__main__':
    app.run(debug=True)