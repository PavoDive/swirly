# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 PavoDive


import yaml
import os


LESSON_PATH = "swirly/lessons"


def list_lessons():
    return [
        f[:-5]
        for f in os.listdir(LESSON_PATH)
        if f.endswith(".yaml")
    ]


class Lesson:
    def __init__(self, steps, metadata=None):
        self.metadata = metadata or {}
        self.steps = steps

    @staticmethod
    def load(path):
        with open(path) as f:
            raw = yaml.safe_load(f)
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
