from langchain_core.runnables import RunnableLambda, RunnableParallel


def test1(x: int):
    return x + 10


r1 = RunnableLambda(test1)

res = r1.invoke(4)
print(f"res: {res}")

# 2、批量调用
batchRes = r1.batch([4, 5])
print(f"batchRes: {batchRes}")


def test2(prompt: str):
    for item in prompt.split(' '):
        yield item


# 3. 流式输出
streamRunnable = RunnableLambda(test2)
streamRes = streamRunnable.stream('This is a Dog.')

for chunk in streamRes:
    print(chunk)

# 4. 组合链
r2 = RunnableLambda(lambda x: x * 2)
combinedChain = r1 | r2  # 串行

combinedRes = combinedChain.invoke(2)
print(f"combinedRes: {combinedRes}")

# 5.并行运行
parallelChain = RunnableParallel(r1=r1, r2=r2)

# max_concurrency: 最大并发数
parallelRes = parallelChain.batch([1, 2, 3, 4], config={'max_concurrency': 1})
print(f"parallelRes: {parallelRes}")