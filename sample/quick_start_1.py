from langchain_core.runnables import RunnableLambda


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


streamRunnable = RunnableLambda(test2)
streamRes = streamRunnable.stream('This is a Dog.')

for chunk in streamRes:
    print(chunk)
