from langchain_core.runnables import RunnableLambda

counter = -1  # 计数用的


def test3(x):
    global counter
    counter += 1
    print(f'执行了 {counter} 次')
    return x / counter


# stop_after_attempt 是总尝试次数，不是重试次数
# 当这个 Runnable 抛出异常时，自动重新执行，直到成功，但最多总共执行 2 次（包含第一次调用 + 后续重试）。
r1 = RunnableLambda(test3)
# case1 = r1.with_retry(stop_after_attempt=2)
# print(f"case1.invoke(2): {case1.invoke(2)}")

# 只对特定异常重试（比如只对网络超时重试，不对除零重试）
# case2 = r1.with_retry(
#     stop_after_attempt=4,
#     retry_if_exception_type=(TimeoutError, ConnectionError)
# )
#
# # throw ZeroDivisionError: division by zero
# print(f"case2.invoke(2): {case2.invoke(2)}")

# 每次重试之间加等待（指数退避：1s, 2s, 4s, 8s...）
case3 = r1.with_retry(
    stop_after_attempt=4,
    retry_if_exception_type=(ZeroDivisionError, TimeoutError, ConnectionError),
    wait_exponential_jitter=True  # 随机抖动，避免重试时间相同
)
print(f"case3.invoke(2): {case3.invoke(2)}")
