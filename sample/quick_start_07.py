from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

from sample.util.my_llm import llm

# ==========================================
# ① 声明式配置：新增领域只改这里
# ==========================================
EXPERTS = {
    'physics': {
        'keywords': ['物理'],
        'template': '你是一位物理学教授，擅长用简洁易懂的方式回答物理问题。问题：{input}',
    },
    'math': {
        'keywords': ['数学'],
        'template': '你是一位数学家，擅长分步骤解决数学问题。问题：{input}',
    },
    'history': {
        'keywords': ['历史'],
        'template': '你是一位历史学家，对历史事件和背景有深入研究。问题：{input}',
    },
    'computer_science': {
        'keywords': ['计算机'],
        'template': '你是一位计算机科学专家，擅长算法、数据结构和编程。问题：{input}',
    },
}
# DEFAULT_TEMPLATE：用明确指令句 + 禁止行为约束，防止 LLM 自由发挥
DEFAULT_TEMPLATE = (
    "你是一个智能路由助手。用户的问题：{input}\n"
    "该问题不属于任何已分类的专家领域（物理/数学/历史/计算机）。\n"
    "请明确告知用户：'抱歉，我暂时没有针对此类问题的专家角色，请换一个领域的问题试试。'\n"
    "不要尝试回答用户的原始问题。"
)

# ==========================================
# ② 用循环自动创建所有 chain（末尾统一加 StrOutputParser）
# ==========================================
chains = {
    name: ChatPromptTemplate.from_template(expert['template']) | llm | StrOutputParser()
    for name, expert in EXPERTS.items()
}
chains['default'] = ChatPromptTemplate.from_template(DEFAULT_TEMPLATE) | llm | StrOutputParser()


# ==========================================
# ③ 工厂函数：生成条件闭包
# ==========================================
def make_condition(keywords):
    print(f"make_condition -> {keywords}")

    def condition(input):
        print(f"condition -> {input}")
        return any(kw in input['type'] for kw in keywords)

    return condition


# ==========================================
# ④ RunnableBranch：前面全是 (条件, chain) tuple，最后一个非 tuple 是 default
# ==========================================
branch = RunnableBranch(
    *[(make_condition(expert['keywords']), chains[name]) for name, expert in EXPERTS.items()],
    chains['default']
)

# ==========================================
# ⑤ 测试
# ==========================================
if __name__ == '__main__':
    # 测试1：能归类到物理 → 走 physics_chain
    r1 = branch.invoke({'type': '物理', 'input': '为什么天空是蓝色的？'})
    print(f"物理测试: {r1}\n")

    # 测试2：无法归类 → 走 default_chain
    r2 = branch.invoke({'type': '其他', 'input': '韩红是个骗子吗？'})
    print(f"兜底测试: {r2}\n")
