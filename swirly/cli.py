# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 Your Name


from swirly.env import LessonEnv
from swirly.engine import dispatch
from swirly.lesson import Lesson
import pandas as pd  # preload for user
import os
from pandas import Series, DataFrame, Index
from swirly.commands import info
import numpy as np


def is_equal(a, b):
    if isinstance(a, (Series, DataFrame)) and isinstance(b, type(a)):
        return a.equals(b)
    if isinstance(a, (np.ndarray, Index)) and isinstance(b, type(a)):
        return np.array_equal(a, b)
    return a == b


def is_exploratory_input(s: str) -> bool:
    stripped = s.strip()
    return (
        stripped.startswith("help(")
        or stripped.startswith("?")
        or stripped.startswith("dir(")
    )


def main():
    state_file = ".swirly.state"
    if os.path.exists(state_file):
        env = LessonEnv.load(state_file)
        info(env)
        lesson = Lesson.load(f"swirly/lessons/{env.lesson}.yaml")
        print(f"🔄 Resuming lesson: {env.lesson}\n")
    else:
        from swirly.lesson import list_lessons
        lessons = list_lessons()
        print("📓 Available lessons:")
        for i, name in enumerate(lessons):
            print(f"{i+1}. {name}")

        choice = input("Select lesson by number: ").strip()
        try:
            index = int(choice) - 1
            lesson_name = lessons[index]
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return

        env = LessonEnv()
        info(env)
        env.lesson = lesson_name
        lesson = Lesson.load(f"swirly/lessons/{lesson_name}.yaml")
        env.save(state_file)

        if lesson.metadata.get("preamble"):
            try:
                exec(lesson.metadata["preamble"], env.vars)
            except Exception as e:
                print(f"⚠️ Failed to run lesson preamble: {e}")

    env.vars['pd'] = pd

    while True:
        step = lesson.current_step(env.progress)
        if not step:
            print("🎉 Lesson complete!")
            if os.path.isfile(state_file):
                os.remove(state_file)
            break

        print(f"\n👉 {step['prompt']}")
        user_input = input("R> ")

        if is_exploratory_input(user_input):
            if not is_exploratory_input(step["answer"]):
                try:
                    result = eval(user_input, env.vars)
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"⚠️ {e}")
                continue

        if dispatch(user_input, env):
            continue

        try:
            is_expr = False
            try:
                code = compile(user_input, "<string>", "eval")
                result = eval(code, env.vars)
                if result is not None:
                    print(f"{result}")
                is_expr = True
            except SyntaxError:
                exec(user_input, env.vars)
                var = step.get("var")
                result = env.vars.get(var) if var else None

            expected_expr = step["answer"]
            try:
                compiled = compile(expected_expr, "<string>", "eval")
                expected_result = eval(compiled, env.vars)
            except SyntaxError:
                exec(expected_expr, env.vars)
                var = step.get("var")
                expected_result = env.vars.get(var) if var else None

            if is_equal(result, expected_result):
                print("\n✅ Correct!")
                env.progress += 1
                env.save(state_file)
            else:
                print("\n❌ Try again.")
        except Exception as e:
            print(f"⚠️ {e}")


if __name__ == "__main__":
    main()
