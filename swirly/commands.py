# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 Your Name


import sys


def bye(env): sys.exit(0)


def next(env):
    from swirly.lesson import Lesson
    lesson = Lesson.load(f"swirly/lessons/{env.lesson}.yaml")
    step = lesson.current_step(env.progress)

    print(f"💡 Correct answer: {step.get('setup') or step['answer']}")

    code = step.get('setup') or step['answer']

    try:
        exec(code, env.vars)
    except Exception as e:
        print(f"⚠️ Could not execute answer: {e}")

    env.progress += 1
    env.save(".swirly.state")


def play(env):
    print("Entering play mode. Type `.exit` to return.")
    while True:
        try:
            line = input(">>> ")
            if line.strip() == ".exit":
                break
            result = eval(line, env.vars)
            if result is not None:
                print(result)
        except SyntaxError:
            try:
                exec(line, env.vars)
            except Exception as e:
                print(f"⚠️ {e}")


def reveal(env):
    from swirly.lesson import Lesson
    lesson = Lesson.load(f"swirly/lessons/{env.lesson}.yaml")
    step = lesson.current_step(env.progress)
    print(f"💡 Expected answer: {step.get('setup') or step['answer']}")


def info(env):
    print("""
    \nThis is swirly. At any time type 'reveal' if you want to check the right
    answer, 'next' if you want to advance to the next question without
    answering the current one, 'play' if you want to interact freely
    with Python before returning to the lesson, 'info' for this help,
    and 'bye' to exit swirly.\n""")
