from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from sample.util.my_llm import llm

preferences_prompt = ChatPromptTemplate.from_template(
    "用户输入了一些餐厅偏好：{input1}\n"
    "请将用户的偏好总结为清晰的需求："
)

restaurants_prompt = ChatPromptTemplate.from_template(
    "基于用户需求：{input2}\n"
    "请推荐 3 家适合的餐厅，并说明推荐理由："
)

summarize_recommendations_prompt = ChatPromptTemplate.from_template(
    "以下是餐厅推荐和推荐理由：\n{input3}\n"
    "请总结成 2-3 句话，供用户快速参考："
)

chain = preferences_prompt | llm | restaurants_prompt | llm | summarize_recommendations_prompt | llm | StrOutputParser()

response = chain.invoke({'input1': '我喜欢安静的地方， 有素食的餐厅更好，而且价格也不贵。'})
print(f"response: {response}")
