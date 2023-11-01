import os, sys
import openai
import json
import re

# 运行环境初始化
os.environ["http_proxy"] = "http://127.0.0.1:1088" # 请对应修改为你机器上的本地代理地址
os.environ["https_proxy"] = "http://127.0.0.1:1088" # 请对应修改为你机器上的本地代理地址

openai.api_key = "sk-your-openai-key" # Key only for Alfred Call

def stdout_write(output_string: str) -> None:
    output_string = "..." if output_string == "" else output_string
    sys.stdout.write(output_string)

def add_space(s):
    return re.sub(r'(\{\{.*?\}\})', r' \1 ', s)

# 定义基础请求函数
def call_gpt_response(chat_template, chat_prompt, stream_msg=[]):
    # chat_template 模板取自各个模版md文件
    # chat_prompt 提问
    prompt_messages = []
    chat_prompt = chat_template + chat_prompt
    system_content = {"role": "system", "content": "You are a helpful assistant."}
    user_content_final = {"role": "user", "content": chat_prompt}
    prompt_messages.append(system_content)
    
    i = 1
    for msg in stream_msg:
        if i%2 == 1:
            user_content_previous = {"role": "user", "content": msg}
        else:
            user_content_previous = {"role": "system", "content": msg}
        prompt_messages.append(user_content_previous)
        i = i + 1
    
    prompt_messages.append(user_content_final)
    
    response = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo-0613",
    #   model = "gpt-4",
      messages = prompt_messages
    )

    res = json.loads(str(response))
    res_status = res['choices'][0]['finish_reason']
    res_content = res['choices'][0]['message']['content']

    if res_status == 'stop':
        return res_content
    else:
        print('Something wrong:{}'.format(res_status))
        return 999

if __name__ == '__main__':
    # 根据输入参数，调用不同的模版
    input_selection = "".join(sys.argv[1])
    # 自动判断模板选用
    template_type = open("./templates/templates.json", 'r', encoding='utf-8').read()
    template_text = "请按照{}这里的分类，自动判断以下文本对应的一个任务类型，只输出任务类型的英文key值：{}".format(template_type, input_selection)
    # print('calling gpt', template_text, input_selection)
    response = call_gpt_response(template_text, input_selection)
    template = response
    # print('自动模板判断结果:', template)
    # 根据template参数读取对应md文件
    template_text = open("./templates/{}.md".format(template), 'r', encoding='utf-8').read()

    # 发起请求
    response = call_gpt_response(template_text, input_selection)
    response.replace('`', '').replace('\n\n', '\n')
    if template == 'cardgen':
        response = add_space(response)
    stdout_write(response)