from types import FunctionType, ModuleType

from dlai_grader.grading import object_to_grade, test_case
from dlai_grader.types import (grading_function, grading_wrapper,
                               learner_submission)


def part_1(
    learner_mod: learner_submission,
    solution_mod: ModuleType | None = None,
) -> grading_function:
    @object_to_grade(learner_mod, "simple_output")
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
            if res == "hihi":
                t.msg = "Correct output for test case 1"
            elif res == "hihi!":
                t.msg = "Also correct output for test case 1"
            else:
                t.fail()
                t.msg = "Incorrect output for test case 1"
                t.want = "hihi"
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
    @object_to_grade(learner_mod, "multiply")
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
            if res == 15:
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
        "part1": part_1,
        "part2": part_2,
    }
    return grader_dict[part_id]
