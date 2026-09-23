from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from sample.util.my_llm import llm

prompt1 = PromptTemplate.from_template('给我写一篇关于{key_word}的{type}，字数不超过{count}。')

chain1 = prompt1 | llm | StrOutputParser()

resp = chain1.invoke({'key_word': '青春', 'type': '散文', 'count': 400})
print(f'resp: {resp}')