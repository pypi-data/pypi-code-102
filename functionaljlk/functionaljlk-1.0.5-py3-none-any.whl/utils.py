from functionaljlk.result import Result

def gettattrResult(obj, attr) -> Result:
    try:
        return Result.of(getattr(obj, attr))
    except Exception as e:
        return Result.failure(e)
