from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from sample.util.my_llm import llm

def print_chain1(input):
    print(f"type(input): {type(input)}")  # ← 加这行！
    print(f"input: {input}")
    print('--' * 30)
    return {'text_content': input}

prompt1 = PromptTemplate.from_template('给我写一篇关于{key_word}的{type}，字数不超过{count}。')

# RunnableLambda(str) -> 强制转纯 str
chain1 = prompt1 | llm | StrOutputParser() | RunnableLambda(str)

# resp = chain1.invoke({'key_word': '青春', 'type': '散文', 'count': 400})
# print(f'resp: {resp}')

prompt2 = PromptTemplate.from_template('请简单评价一下这篇短文，如果总分是10分，请给这篇短文打分： {text_content}')
#
# chain2 = {'text_content': chain1} | prompt2 | llm | StrOutputParser()
#
# resp2 = chain2.invoke({'key_word': '青春', 'type': '散文', 'count': 400})
# print(f'resp2: {resp2}')

chain3 = chain1 | RunnableLambda(print_chain1) | prompt2 | llm | StrOutputParser()
resp3 = chain3.invoke({'key_word': '青春', 'type': '散文', 'count': 400})
print(f'resp3: {resp3}')
