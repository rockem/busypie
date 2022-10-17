from busypie.func import is_async
from busypie.types import ConditionEvaluator


async def check(condition_evaluator: ConditionEvaluator) -> any:
    if is_async(condition_evaluator):
        return await condition_evaluator()
    return condition_evaluator()


async def negative_check(condition_evaluator: ConditionEvaluator) -> bool:
    if is_async(condition_evaluator):
        result = await condition_evaluator()
        return not result
    return not condition_evaluator()


async def assert_check(condition_evaluator: ConditionEvaluator) -> bool:
    if is_async(condition_evaluator):
        await condition_evaluator()
    else:
        condition_evaluator()
    return True
