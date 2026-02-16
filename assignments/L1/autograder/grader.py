from types import FunctionType, ModuleType

from dlai_grader.grading import object_to_grade, test_case
from dlai_grader.types import (grading_function, grading_wrapper,
                               learner_submission)


def part_1(
    learner_mod: learner_submission,
    solution_mod: ModuleType | None = None,
) -> grading_function:
    @object_to_grade(learner_mod, "learner_func")
    def g(learner_func: FunctionType) -> list[test_case]:
        cases: list[test_case] = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.fail()
            t.msg = "learner_func has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        try:
            res = learner_func()
            if res == "hello world":
                t.msg = "Correct output for test case 1"
            else:
                t.fail()
                t.msg = "Incorrect output for test case 1"
                t.want = "hello world"
                t.got = res
            cases.append(t)
        except Exception as e:
            t.fail()
            t.msg = f"Error when calling learner_func. Details:\n{e!s}"
            return [t]

        return cases

    return g


def part_2(
    learner_mod: learner_submission,
    solution_mod: ModuleType | None = None,
) -> grading_function:
    @object_to_grade(learner_mod, "add")
    def g(learner_func: FunctionType) -> list[test_case]:
        cases: list[test_case] = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.fail()
            t.msg = "learner_func has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        try:
            res = learner_func(3, 5)
            if res == 8:
                t.msg = "Correct output for test case 2"
            else:
                t.fail()
                t.msg = "Incorrect output for test case 2"
                t.got = res
            cases.append(t)
        except Exception as e:
            t.fail()
            t.msg = f"Error when calling learner_func. Details:\n{e!s}"
            return [t]

        return cases

    return g


def handle_part_id(part_id: str) -> grading_wrapper:
    grader_dict: dict[str, grading_wrapper] = {
        "123": part_1,
        "456": part_2,
    }
    return grader_dict[part_id]
