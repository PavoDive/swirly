# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 PavoDive


import yaml
import importlib.resources


# LESSON_PATH = "swirly/lessons"


def list_lessons():
    lesson_dir = importlib.resources.files("swirly.lessons")
    return [
        f.stem for f in lesson_dir.iterdir()
        if f.suffix == ".yaml"
    ]


def load_lesson_file(name):
    print(name)
    with importlib.resources.files("swirly.lessons").joinpath(
            name).open("r") as f:
        return yaml.safe_load(f)


class Lesson:
    def __init__(self, steps, metadata=None):
        self.metadata = metadata or {}
        self.steps = steps

    @staticmethod
    def load(name):
        print(name)
        raw = load_lesson_file(name)
        if "steps" in raw:
            metadata = dict(raw)
            steps = metadata.pop("steps")
        else:
            metadata = None
            steps = raw

        return Lesson(steps=steps, metadata=metadata)

    def current_step(self, progress):
        if progress >= len(self.steps):
            return None
        return self.steps[progress]
