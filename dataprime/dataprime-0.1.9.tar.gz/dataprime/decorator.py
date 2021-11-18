from functools import wraps

from dataprime.params import EXAMPLES


def param_check(func):
    """参数校验装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
            print(f"调用错误, 请检查参数, 正确参数示例:\n{EXAMPLES.get(func.__name__)}")

    return wrapper

