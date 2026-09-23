import time

from langchain_core.tracers import Run
from langchain_core.runnables import RunnableLambda


# 生命周期管理，单位是秒
def test4(n: int):
    time.sleep(n)
    return n * 2


def on_start(run_obj: Run):
    """ 当r1节点启动的时候，自动调用 """
    print('r1启动的时间： ', run_obj.start_time)


def on_end(run_obj: Run):
    """ 当r1节已经运行结束的时候，自动调用 """
    print('r1结束的时间： ', run_obj.end_time)


def on_error(run_obj: Run):
    print(f"❌ 出错了！异常类型: {type(run_obj.error).__name__}, 详情: {run_obj.error}")


r1 = RunnableLambda(test4)

chain = r1.with_listeners(on_start=on_start, on_end=on_end, on_error=on_error)
resp = chain.invoke(10)
print(f"resp: {resp}")
