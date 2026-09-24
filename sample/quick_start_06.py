from langchain_core.runnables import RunnableLambda, RunnableBranch


def test1(x: int):
    return x + 10


r1 = RunnableLambda(test1)
r2 = RunnableLambda(lambda x: [x] * 2)

branch = RunnableBranch(
    (lambda x: x > 12, r2),  # tuple → 条件分支 1
    RunnableLambda(lambda x: {'key': x}),  # 非 tuple → default 兜底
)

chain = r1 | branch
response = chain.invoke(1)
print(f"response: {response}")
